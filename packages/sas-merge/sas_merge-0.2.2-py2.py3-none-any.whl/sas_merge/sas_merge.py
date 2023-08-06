from pyspark.sql.functions import col,sequence,when,to_date,months_between,substring,year as _year, month as _month,coalesce,expr,row_number,desc,lit,sum as _sum,round as _round,expr,array_repeat,explode, max as _max, greatest as _greatest,udf, monotonically_increasing_id,concat
from pyspark.sql.window import Window


def SAS_merge(df1,df2,join_type,join_key):
    if not isinstance(join_key, list):
        raise TypeError("join_key must be a list")
    tablea = df1 
    tableb = df2
    if join_type not in ["left","right","inner","full"]:
        raise ValueError("please use one of left, right, inner, full as join type")
    #add id for sorting purpose
    tablea = tablea.withColumn(
        "idx",
        row_number().over(Window.orderBy(monotonically_increasing_id()))+10)
    tableb = tableb.withColumn(
        "idx",
        row_number().over(Window.orderBy(monotonically_increasing_id())))


    #get join exclusion list
    ##prepare for final union
    df_left_exclude = tablea.join(tableb,join_key,"left_anti")
    df_right_exclude = tableb.join(tablea,join_key,"left_anti")
    df_left_exclusion_list = df_left_exclude.withColumn("key_concat",concat(*join_key)).select("key_concat").rdd.flatMap(lambda x: x).collect()
    df_right_exclusion_list = df_right_exclude.withColumn("key_concat",concat(*join_key)).select("key_concat").rdd.flatMap(lambda x: x).collect()
    df_exclustion = df_left_exclusion_list.copy() + df_right_exclusion_list.copy()
    if join_type == "left": 
        df_exclude = df_left_exclude.drop("idx")
    if join_type == "right":
        df_exclude = df_right_exclude.drop("idx")
    if join_type == "inner":
        df_exclude = None
    if join_type == "full":
        df_exclude = df_left_exclude.unionByName(df_right_exclude,allowMissingColumns=True).drop("idx")

    tablea_groupby = tablea.groupby(join_key).count().withColumnRenamed("count","tablea_count").withColumn("key_concat",concat(*join_key))
    tableb_groupby = tableb.groupby(join_key).count().withColumnRenamed("count","tableb_count").withColumn("key_concat",concat(*join_key))
    #take out the unique keys
    tablea_groupby = tablea_groupby.filter(~col("key_concat").isin(set(df_exclustion))).drop("key_concat")
    tableb_groupby = tableb_groupby.filter(~col("key_concat").isin(set(df_exclustion))).drop("key_concat")
    #find the max count
    df_table = tablea_groupby.join(tableb_groupby,join_key,"left").withColumn("max_count",_greatest(col("tablea_count"),col("tableb_count")))


    #create common and uncommon column headers
    tablea_columns = tablea.columns
    tableb_columns = tableb.columns
    common_columns = list(set(tablea_columns).intersection(tableb_columns))
    common_columns_wokey = common_columns.copy()
    common_columns_wokey = [x for x in common_columns_wokey if x not in join_key]
    uncommon_columns = list(set(tablea_columns).symmetric_difference(tableb_columns))
    uncommon_tablea_columns = list(set(tablea_columns).symmetric_difference(common_columns_wokey))
    uncommon_tableb_columns = list(set(tableb_columns).symmetric_difference(common_columns_wokey))  
    #create TableA and TableB common field based on the max_count
    #filter when the max count is from either TableA or AableB
  
    df_tableb = df_table.filter(df_table.max_count==df_table.tableb_count)
    #filter out when max count equals both left and right
    df_common_left = df_table.where(df_table.max_count!=df_table.tableb_count)
    df_tablea = df_common_left.filter(df_table.max_count==df_table.tablea_count)
    tablea_common = df_tablea.join(tablea.select(common_columns),join_key,"left")#use common A table index
    tableb_common = df_tableb.join(tableb.select(common_columns),join_key,"left")#use common B table index
    table_combined = tablea_common.unionByName(tableb_common)

    table_combined = table_combined.sort([*join_key,"idx"]).select(common_columns)
    #table_combined is the combined result with commmon key (contract)
    #the idx comes from either tableA or tableB depends on where the max records are from.

    table_combined_key = Window.partitionBy(join_key).orderBy("idx")
    #create key based row number for the unique identifier
    table_combined = table_combined.withColumn("row",row_number().over(table_combined_key))
    #table combined at this stage has two indexes, 
    #1 idx from either TableA or TableB depends on max, 
    #2 row as row index based on key
    # # the indexing used here is row index  
    uncommon_key = uncommon_columns.copy()
    uncommon_key.extend(join_key)
    table_uncommon_key = Window.partitionBy(join_key).orderBy(*join_key,"idx") #drop idx later to avoid mixing the order.
    tablea_uncommon_row = tablea.withColumn("row",row_number().over(table_uncommon_key)).drop("idx").select(uncommon_tablea_columns +["row"])
    tableb_uncommon_row = tableb.withColumn("row",row_number().over(table_uncommon_key)).drop("idx").select(uncommon_tableb_columns + ["row"])

    #left join with combined table to form uncommon fields
    table_concat = table_combined.join(tablea_uncommon_row,[*join_key,"row"],"left").sort(*join_key,"idx")
    table_concat_2 = table_concat.join(tableb_uncommon_row,[*join_key,"row"],"left").sort(*join_key,"idx")
    tablea_uncom_gap = table_combined.join(tablea_uncommon_row,[*join_key,"row"],"left_anti").sort(*join_key,"idx")
    tableb_uncom_gap = table_combined.join(tableb_uncommon_row,[*join_key,"row"],"left_anti").sort(*join_key,"idx")
    table_uncommon_group = Window.partitionBy(join_key).orderBy(*join_key,desc("row"))
    #value to be used for back fill
    tablea_uncommon_row_desc = tablea_uncommon_row.withColumn("row_2",row_number().over(table_uncommon_group)).filter(col("row_2") == 1).drop("row_2","row")
    tableb_uncommon_row_desc = tableb_uncommon_row.withColumn("row_2",row_number().over(table_uncommon_group)).filter(col("row_2") == 1).drop("row_2","row")
    #add row into the uncommon column list
    uncommon_tablea_columns_row = uncommon_tablea_columns.copy()
    uncommon_tablea_columns_row.append("row")
    uncommon_tableb_columns_row = uncommon_tableb_columns.copy()
    uncommon_tableb_columns_row.append("row")
    #uncommon column names without row and contract account
    uncommon_tablea_columns_only = uncommon_tablea_columns.copy()
    uncommon_tablea_columns_only = [x for x in uncommon_tablea_columns_only if x not in join_key]
    uncommon_tableb_columns_only = uncommon_tableb_columns.copy()
    uncommon_tableb_columns_only = [x for x in uncommon_tableb_columns_only if x not in join_key]
    #form a new backfill dataframe
    tablea_uncommon_filled = tablea_uncom_gap.join(tablea_uncommon_row_desc,join_key,"left").select([col(x) for x in uncommon_tablea_columns_row])
    tableb_uncommon_filled = tableb_uncom_gap.join(tableb_uncommon_row_desc,join_key,"left").select([col(x) for x in uncommon_tableb_columns_row])
    #avoid ambiguous naming
    #change_2 naming to _2_ to avoid _2 in column header and creating ambiuous naming again
    for val in uncommon_tablea_columns_only:
        tablea_uncommon_filled = tablea_uncommon_filled.withColumnRenamed(val,(val+"_2_"))
    for val in uncommon_tableb_columns_only:
        tableb_uncommon_filled = tableb_uncommon_filled.withColumnRenamed(val,(val+"_2_"))
    #avoid joining with empty dataset
    if tablea_uncommon_filled.rdd.isEmpty() == False:
        table_concat_2 = table_concat_2.join(tablea_uncommon_filled,[*join_key,"row"],"left").sort(*join_key,"idx")
    if tableb_uncommon_filled.rdd.isEmpty() == False:
        table_concat_2 = table_concat_2.join(tableb_uncommon_filled,[*join_key,"row"],"left").sort(*join_key,"idx")
    table_concat_full = table_concat_2.alias("table_concat_full")
    #merge two columns for backfilling
    #only merge when daaset is not empty
    if tablea_uncommon_filled.rdd.isEmpty() == False:
        for val in uncommon_tablea_columns_only:
            table_concat_full = table_concat_full.withColumn(val,coalesce(col(val),col(val+"_2_"))).drop(val+"_2_")

    if tableb_uncommon_filled.rdd.isEmpty() == False:
        for val in uncommon_tableb_columns_only:
            table_concat_full = table_concat_full.withColumn(val,coalesce(col(val),col(val+"_2_"))).drop(val+"_2_")

    table_uncommon_merge = table_concat_full.alias("table_uncommon_merge")
    ###tablea still maintain the right order so we don't need to join with idx to override.
    #rename to avoid duplications
    common_columns_only = common_columns_wokey.copy()
    common_columns_only.remove("idx")
    tableb_common_override = df_tablea.join(tableb.select(common_columns),join_key,"inner").select(common_columns)
    #rename to avoid ambiguous column naming
    for val in common_columns_only:
        tableb_common_override = tableb_common_override.withColumnRenamed(val,(val+"_2_")).sort(*join_key,"idx")
    #create row number for proper indexing
    comm_override_index = Window.partitionBy(join_key).orderBy(*join_key,"idx")
    tableb_common_override = tableb_common_override.withColumn("row",row_number().over(comm_override_index)).drop("idx")
    #create a new override column
    table_override = table_uncommon_merge.join(tableb_common_override,[*join_key,"row"],"left").sort(*join_key,"row")
    #merge the result and drop
    if common_columns_only == []:
        #no common_columns
        table_shared_combined = table_override.drop("row","idx")
    else:
        for val in common_columns_only:      
            table_override = table_override.withColumn(val,coalesce(col(val+"_2_"),col(val))).drop(val+"_2_")
        table_shared_combined = table_override.drop("row","idx")

    if df_exclude == None:
        #inner join, don't need to stack
        return  table_shared_combined
    else:
        df_final = table_shared_combined.unionByName(df_exclude, allowMissingColumns=True)
        return df_final


