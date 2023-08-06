#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np   
import pandas as pd
from itertools import chain
from itertools import permutations 
from collections import Counter
import datetime
from functools import reduce
dotprod = lambda K, L: reduce(lambda z1, z2: z1+z2, map(lambda x: reduce(lambda x1, x2: x1*x2, x), zip(K, L))) if len(K)==len(L) else 0



# 1. num_rows : number of rows in the payoff matrix. Integer
# 2. num_cols : number of columns in the payoff matrix. Integer
# 3. memory_length : How much history need to consider. Integer 
# 4. iterate_all : Whether to consider all possible combinations of history or specific. "YES" or "NO"
# 5. initial_history : Valid when iterate_all = NO. A list of initial history. Sepcify as [[0,1],[1,2]]. This means the first period
# outcome is first strategy for row player and second strategy for column player.
# The second period outcome is second strategy for row player and 3rd strategy for column player.
# Please note these are the positions of the strategies in the payoff matrix. And NOT the payoff values.
# Here we have specified 2 period histories. Therefore, memory_length should be 2.

# 6.timeperiod: For how much time period, iterations required to run? Integer.
# 7.iteration_name: Give any name for this iterations. String
# 8.row_player_payoffs. List of row player payoffs. To be specified as first row payoff, second row payoffs, and so on.. E.g.[2,0,2,5] 
# implies first row payoffs for row player are 2 and 0 against first and second strategy of the column player.
# second row payoffs for row player are 2 and 5. This is assuming we have 2*2 payoff matrix.
# 9.column_player_payoffs. Same as row_player_payoffs. But this specifies the column player payoffs. List is the required format
# 10.path_to_save_output. the location where output excel files should be saved.



def simulation_function(num_rows,
                        num_cols,
                        memory_length,
                        iterate_all,
                        initial_history,
                        timeperiod,
                        iteration_name,
                        row_player_payoffs,
                        column_player_payoffs,
                        path_to_save_output
                       ):
    num_rows = num_rows
    num_cols = num_cols
    memory_length = memory_length  
    iterate_all = iterate_all

    initial_history = initial_history

    timeperiod = timeperiod
    iteration_name = iteration_name
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") 
    empty_matrix_row = np.zeros((num_rows,num_cols))
    empty_matrix_column = np.zeros((num_rows,num_cols))

    row_to_fill = row_player_payoffs
    m=0
    for j in range(num_rows):
        for k in range(num_cols):
            empty_matrix_row[j,k] = row_to_fill[m]
            m+=1

    col_to_fill = column_player_payoffs
    
    m=0
    for j in range(num_rows):
        for k in range(num_cols):
            empty_matrix_column[j,k] = col_to_fill[m]
            m+=1


    history_payoffs = [[] for i in range(memory_length)]
    range_lists = [[*range(num_rows)],[*range(num_cols)]]

    foo_cart_prod = [[a,b] for a in range_lists[0] for b in range_lists[1]]
    total_permutations = list(permutations(foo_cart_prod,memory_length))

    additional_elements_to_fill = []

    if memory_length > 1:
        for uu in range(len(foo_cart_prod)):
            additional_elements_to_fill.append(tuple([foo_cart_prod[uu]]*memory_length))


    total_permutations.extend(additional_elements_to_fill)

    if iterate_all == "NO":
        trend_db_to_store = pd.DataFrame(columns=["keys","initial_history","count1","timeperiod"])
        
        for vv in range(memory_length):
            history_payoffs[vv] = initial_history[vv]
            
        TimePeriodCart_prod_store = []
        cart_prod2 = [history_payoffs]
        for t in range(timeperiod):
            tempcart1 = []
            tempcart2 = []

            for j in range(len(cart_prod2)):

                distinct_elements_for_row = []
                distinct_elements_for_column = []
                for i in range(memory_length):
                    xx = cart_prod2[j][i][1]
                    distinct_elements_for_row.append(xx)
                    xx = cart_prod2[j][i][0]
                    distinct_elements_for_column.append(xx)
                distinct_elements_for_row = list(set(distinct_elements_for_row))
                distinct_elements_for_column = list(set(distinct_elements_for_column))

                fill_best_response_for_row = []
                for z in range(len(distinct_elements_for_row)):
                    temp_payoffs = []
                    for l in range(num_rows):
                        xx = empty_matrix_row[l,distinct_elements_for_row[z]]
                        temp_payoffs.append(xx)
                    fill_best_response_for_row.append([k for k, m in enumerate(temp_payoffs) if m == max(temp_payoffs)])

                fill_best_response_for_column = []
                for z in range(len(distinct_elements_for_column)):
                    temp_payoffs = []
                    for l in range(num_cols):
                        xx = empty_matrix_column[distinct_elements_for_column[z],l]
                        temp_payoffs.append(xx)
                    fill_best_response_for_column.append([k for k, m in enumerate(temp_payoffs) if m == max(temp_payoffs)])

                flat_list_column = [item for sublist in fill_best_response_for_column for item in sublist]
                flat_list_row = [item for sublist in fill_best_response_for_row for item in sublist]
                flat_list_row = list(set(flat_list_row))
                flat_list_column = list(set(flat_list_column))

                somelists = [flat_list_row,flat_list_column]
                cart_prod = [[a,b] for a in somelists[0] for b in somelists[1]]

                if len(cart_prod2[j]) > 1:
                    history_payoffs_aggregated = cart_prod2[j][1:]
                else:
                    history_payoffs_aggregated = [cart_prod2[j][0]]

                somelists = [[history_payoffs_aggregated[-1]],cart_prod]
            
                cart_prod2_intermediate = [[a,b] for a in somelists[0] for b in somelists[1]]
                
                if len(history_payoffs_aggregated) > 1:
                    cart_prod2_intermediate2 = [history_payoffs_aggregated[:-1] + i for i in cart_prod2_intermediate]
                else:
                    cart_prod2_intermediate2 = cart_prod2_intermediate

                tempcart1.append(cart_prod)
                tempcart2.append(cart_prod2_intermediate2)

            TimePeriodCart_prod_store.append(tempcart1)
            items2 = list(chain.from_iterable(tempcart2))
            cart_prod2 = items2
            #print(t)
        
        flat_list_db = [item for sublist in TimePeriodCart_prod_store for item in sublist]
        flat_list_db2 = [item for sublist in flat_list_db for item in sublist]
        flat_list_db3 = [str(i) for i in flat_list_db2]
        cc = Counter(flat_list_db3)
        d=dict(cc)
        foo = pd.DataFrame([d],columns=d.keys()).T
        foo.columns = ["count"]
        foo = foo.sort_values(by="count",ascending=False)
        foo["keys"] = foo.index.tolist()
        foo["initial_history"] = str(tuple(history_payoffs))
        foo = foo.reset_index(drop=True)
        
        #### in % 
        foo["count"] = foo["count"]/sum(foo["count"])
        foo["count"] = round(foo["count"]*100,2)
        
        
        ###
        foo["iteration_name"] = iteration_name
        foo["MemorySize"] = memory_length
        foo["TimePeriod"] = timeperiod
        foo["num_rows"] = num_rows
        foo["num_cols"] = num_cols
        foo["iterate_all"] = iterate_all
        ###
        
        foo.to_excel(path_to_save_output+"selected_iteration_data_"+iteration_name+"_"+today+".xlsx",index=None)
        
        ######## timeperiod #####
        
        for uuu in range(len(TimePeriodCart_prod_store)):
            
            flat_list_db2_last = [item for sublist in TimePeriodCart_prod_store[uuu] for item in sublist]
            flat_list_db3_last = [str(i) for i in flat_list_db2_last]
            cc = Counter(flat_list_db3_last)
            d=dict(cc)
        
            foo_last = pd.DataFrame([d],columns=d.keys()).T
            foo_last.columns = ["count"]
            foo_last = foo_last.sort_values(by="count",ascending=False)
            foo_last["keys"] = foo_last.index.tolist()
            foo_last["initial_history"] = str(tuple(history_payoffs))
            foo_last["count1"] = foo_last["count"]/sum(foo_last["count"])
            foo_last["count1"] = round(foo_last["count1"]*100,2)
            foo_last = foo_last[["keys","initial_history","count1"]]
            foo_last["timeperiod"] = uuu
            trend_db_to_store = trend_db_to_store.append(foo_last,ignore_index=True)
        
        
        
        trend_db_to_store["iteration_name"] = iteration_name
        trend_db_to_store["MemorySize"] = memory_length
        trend_db_to_store["TimePeriod"] = timeperiod
        trend_db_to_store["num_rows"] = num_rows
        trend_db_to_store["num_cols"] = num_cols
        trend_db_to_store["iterate_all"] = iterate_all
        
        trend_db_to_store.to_excel(path_to_save_output+"selected_iteration_data_timperiod_"+iteration_name+"_"+today+".xlsx",index=None)
        
        
        foorows = pd.DataFrame(empty_matrix_row)
        foocolumns = pd.DataFrame(empty_matrix_column)
        list_to_fill = []
        for i in range(num_rows):
            for j in range(num_cols):
                xxx = foorows.iloc[i][j]
                yyy = foocolumns.iloc[i][j]
                list_to_fill.append((xxx,yyy))


        emptypd_to_fill = foorows.copy()
        for i in range(num_rows):
            for j in range(num_cols):
                rowextract = np.array_split(list_to_fill,num_rows)[i].tolist()
                emptypd_to_fill.loc[i,j] = str(rowextract[j])

        
        emptypd_to_fill["iteration_name"] = iteration_name
        emptypd_to_fill["MemorySize"] = memory_length
        emptypd_to_fill["TimePeriod"] = timeperiod
        emptypd_to_fill["num_rows"] = num_rows
        emptypd_to_fill["num_cols"] = num_cols
        emptypd_to_fill["iterate_all"] = iterate_all
        
        
        emptypd_to_fill.to_excel(path_to_save_output+"selected_iteration_data_payoffmatrix_"+iteration_name+"_"+today+".xlsx")
    
    if iterate_all == "YES":
        foo_to_fill = pd.DataFrame(columns=['count','keys','initial_history'])
        trend_db_to_store = pd.DataFrame(columns=["keys","initial_history","count1","timeperiod"])
        
        for zz in range(len(total_permutations)):
            for vv in range(memory_length):
                history_payoffs[vv] = total_permutations[zz][vv]

            TimePeriodCart_prod_store = []
            cart_prod2 = [history_payoffs]
            for t in range(timeperiod):
                tempcart1 = []
                tempcart2 = []

                for j in range(len(cart_prod2)):

                    distinct_elements_for_row = []
                    distinct_elements_for_column = []
                    for i in range(memory_length):
                        xx = cart_prod2[j][i][1]
                        distinct_elements_for_row.append(xx)
                        xx = cart_prod2[j][i][0]
                        distinct_elements_for_column.append(xx)
                    distinct_elements_for_row = list(set(distinct_elements_for_row))
                    distinct_elements_for_column = list(set(distinct_elements_for_column))

                    fill_best_response_for_row = []
                    for z in range(len(distinct_elements_for_row)):
                        temp_payoffs = []
                        for l in range(num_rows):
                            xx = empty_matrix_row[l,distinct_elements_for_row[z]]
                            temp_payoffs.append(xx)
                        fill_best_response_for_row.append([k for k, m in enumerate(temp_payoffs) if m == max(temp_payoffs)])

                    fill_best_response_for_column = []
                    for z in range(len(distinct_elements_for_column)):
                        temp_payoffs = []
                        for l in range(num_cols):
                            xx = empty_matrix_column[distinct_elements_for_column[z],l]
                            temp_payoffs.append(xx)
                        fill_best_response_for_column.append([k for k, m in enumerate(temp_payoffs) if m == max(temp_payoffs)])

                    flat_list_column = [item for sublist in fill_best_response_for_column for item in sublist]
                    flat_list_row = [item for sublist in fill_best_response_for_row for item in sublist]
                    flat_list_row = list(set(flat_list_row))
                    flat_list_column = list(set(flat_list_column))

                    somelists = [flat_list_row,flat_list_column]
                    cart_prod = [[a,b] for a in somelists[0] for b in somelists[1]]

                    
                    if len(cart_prod2[j]) > 1:
                        history_payoffs_aggregated = cart_prod2[j][1:]
                    else:
                        history_payoffs_aggregated = [cart_prod2[j][0]]

                    somelists = [[history_payoffs_aggregated[-1]],cart_prod]
                    cart_prod2_intermediate = [[a,b] for a in somelists[0] for b in somelists[1]]
                    
                    if len(history_payoffs_aggregated) > 1:
                        cart_prod2_intermediate2 = [history_payoffs_aggregated[:-1] + i for i in cart_prod2_intermediate]
                    else:
                        cart_prod2_intermediate2 = cart_prod2_intermediate
            

                    tempcart1.append(cart_prod)
                    tempcart2.append(cart_prod2_intermediate2)

                TimePeriodCart_prod_store.append(tempcart1)
                items2 = list(chain.from_iterable(tempcart2))
                cart_prod2 = items2
        
            flat_list_db = [item for sublist in TimePeriodCart_prod_store for item in sublist]
            flat_list_db2 = [item for sublist in flat_list_db for item in sublist]
            flat_list_db3 = [str(i) for i in flat_list_db2]
            cc = Counter(flat_list_db3)
            d=dict(cc)
            foo = pd.DataFrame([d],columns=d.keys()).T
            foo.columns = ["count"]
            foo = foo.sort_values(by="count",ascending=False)
            
            foo["keys"] = foo.index.tolist()
            foo["initial_history"] = str(total_permutations[zz])
            foo = foo.reset_index(drop=True)
            
            
            ##### get in % #####
            foo["count"] = foo["count"]/sum(foo["count"])
            foo["count"] = round(foo["count"]*100,2)
            
            
            foo_to_fill = foo_to_fill.append(foo,ignore_index=True)
            #print(zz)
            
          ###### Get trend ###
        
            for uuu in range(len(TimePeriodCart_prod_store)):
                
                flat_list_db2_last = [item for sublist in TimePeriodCart_prod_store[uuu] for item in sublist]
                flat_list_db3_last = [str(i) for i in flat_list_db2_last]
                cc = Counter(flat_list_db3_last)
                d=dict(cc)
                foo_last = pd.DataFrame([d],columns=d.keys()).T
                foo_last.columns = ["count"]
                foo_last = foo_last.sort_values(by="count",ascending=False)
                foo_last["keys"] = foo_last.index.tolist()

                foo_last["initial_history"] = str(total_permutations[zz])
                foo_last = foo_last[["keys","count","initial_history"]]
                
                foo_last["count1"] = foo_last["count"]/sum(foo_last["count"])
                foo_last["count1"] = round(foo_last["count1"]*100,2)
                foo_last = foo_last[["keys","initial_history","count1"]]
                foo_last["timeperiod"] = uuu
                trend_db_to_store = trend_db_to_store.append(foo_last,ignore_index=True)
            
            

        foo_to_fill["iteration_name"] = iteration_name
        foo_to_fill["MemorySize"] = memory_length
        foo_to_fill["TimePeriod"] = timeperiod
        foo_to_fill["num_rows"] = num_rows
        foo_to_fill["num_cols"] = num_cols
        foo_to_fill["iterate_all"] = iterate_all

        foo_to_fill.to_excel(path_to_save_output+"all_iteration_data_"+iteration_name+"_"+today+".xlsx",index=None)


        trend_db_to_store["iteration_name"] = iteration_name
        trend_db_to_store["MemorySize"] = memory_length
        trend_db_to_store["TimePeriod"] = timeperiod
        trend_db_to_store["num_rows"] = num_rows
        trend_db_to_store["num_cols"] = num_cols
        trend_db_to_store["iterate_all"] = iterate_all

        trend_db_to_store.to_excel(path_to_save_output+"all_iteration_data_timperiod_"+iteration_name+"_"+today+".xlsx",index=None)



        foorows = pd.DataFrame(empty_matrix_row)
        foocolumns = pd.DataFrame(empty_matrix_column)
        list_to_fill = []
        for i in range(num_rows):
            for j in range(num_cols):
                xxx = foorows.iloc[i][j]
                yyy = foocolumns.iloc[i][j]
                list_to_fill.append((xxx,yyy))


        emptypd_to_fill = foorows.copy()
        for i in range(num_rows):
            for j in range(num_cols):
                rowextract = np.array_split(list_to_fill,num_rows)[i].tolist()
                emptypd_to_fill.loc[i,j] = str(rowextract[j])



        emptypd_to_fill["iteration_name"] = iteration_name
        emptypd_to_fill["MemorySize"] = memory_length
        emptypd_to_fill["TimePeriod"] = timeperiod
        emptypd_to_fill["num_rows"] = num_rows
        emptypd_to_fill["num_cols"] = num_cols
        emptypd_to_fill["iterate_all"] = iterate_all

        emptypd_to_fill.to_excel(path_to_save_output+"all_iteration_data_payoffmatrix_"+iteration_name+"_"+today+".xlsx")

    return print("done")
    


def simulation_function_payoff(num_rows,
                        num_cols,
                        memory_length,
                        iterate_all,
                        initial_history,
                        timeperiod,
                        iteration_name,
                        row_player_payoffs,
                        column_player_payoffs,
                        path_to_save_output
                       ):
    num_rows = num_rows
    num_cols = num_cols
    memory_length = memory_length  
    iterate_all = iterate_all

    initial_history = initial_history

    timeperiod = timeperiod
    iteration_name = iteration_name
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") 
    empty_matrix_row = np.zeros((num_rows,num_cols))
    empty_matrix_column = np.zeros((num_rows,num_cols))

    row_to_fill = row_player_payoffs
    m=0
    for j in range(num_rows):
        for k in range(num_cols):
            empty_matrix_row[j,k] = row_to_fill[m]
            m+=1

    col_to_fill = column_player_payoffs
    
    m=0
    for j in range(num_rows):
        for k in range(num_cols):
            empty_matrix_column[j,k] = col_to_fill[m]
            m+=1


    history_payoffs = [[] for i in range(memory_length)]
    range_lists = [[*range(num_rows)],[*range(num_cols)]]

    foo_cart_prod = [[a,b] for a in range_lists[0] for b in range_lists[1]]
    total_permutations = list(permutations(foo_cart_prod,memory_length))

    additional_elements_to_fill = []

    if memory_length > 1:
        for uu in range(len(foo_cart_prod)):
            additional_elements_to_fill.append(tuple([foo_cart_prod[uu]]*memory_length))


    total_permutations.extend(additional_elements_to_fill)

    if iterate_all == "NO":
        
        trend_db_to_store = pd.DataFrame(columns=["keys","initial_history","count1","timeperiod"])
        for vv in range(memory_length):
            history_payoffs[vv] = initial_history[vv]

        TimePeriodCart_prod_store = []
        cart_prod2 = [history_payoffs]
        for t in range(timeperiod):
            tempcart1 = []
            tempcart2 = []

            for j in range(len(cart_prod2)):

                distinct_elements_for_row = []
                distinct_elements_for_column = []
                for i in range(memory_length):
                    xx = cart_prod2[j][i][1]
                    distinct_elements_for_row.append(xx)
                    xx = cart_prod2[j][i][0]
                    distinct_elements_for_column.append(xx)
                distinct_elements_for_row = list(set(distinct_elements_for_row))
                distinct_elements_for_column = list(set(distinct_elements_for_column))


                fill_best_response_for_row = []
                for z in range(len(distinct_elements_for_row)):
                    temp_payoffs = []
                    for l in range(num_rows):
                        xx = empty_matrix_row[l,distinct_elements_for_row[z]]
                        temp_payoffs.append(xx)
                    fill_best_response_for_row.append(temp_payoffs)

                probfreq_row = []
                for kk in range(len(cart_prod2[j])):
                    foostorerow = cart_prod2[j][kk][1]
                    probfreq_row.append(foostorerow)


                d = {x:probfreq_row.count(x) for x in probfreq_row}
                foo = pd.DataFrame([d],columns=d.keys()).T
                foo.columns = ["count"]
                foo = foo.sort_values(by="count",ascending=False)
                foo["keys"] = foo.index.tolist()
                foo["prob"] = foo["count"]/memory_length
                foo = foo.sort_values(by="keys")

                reformatted_fill_best_response_for_row = []
                for jj in range(num_rows):
                    xxx = [x[jj] for x in fill_best_response_for_row]
                    reformatted_fill_best_response_for_row.append(xxx)


                best_response_for_row = []
                for pp in range(len(reformatted_fill_best_response_for_row)):
                    xxx = dotprod(reformatted_fill_best_response_for_row[pp],foo['prob'].tolist())
                    best_response_for_row.append(xxx)


                results_to_store_row = []
                results_to_store_row.append([k for k, m in enumerate(best_response_for_row) if m == max(best_response_for_row)])


               

                fill_best_response_for_column = []
                for z in range(len(distinct_elements_for_column)):
                    temp_payoffs = []
                    for l in range(num_cols):
                        xx = empty_matrix_column[distinct_elements_for_column[z],l]
                        temp_payoffs.append(xx)
                    fill_best_response_for_column.append(temp_payoffs)


                probfreq_col = []
                for kk in range(len(cart_prod2[j])):
                    foostorecol = cart_prod2[j][kk][0]
                    probfreq_col.append(foostorecol)


                d = {x:probfreq_col.count(x) for x in probfreq_col}
                foo = pd.DataFrame([d],columns=d.keys()).T
                foo.columns = ["count"]
                foo = foo.sort_values(by="count",ascending=False)
                foo["keys"] = foo.index.tolist()

                foo["prob"] = foo["count"]/memory_length
                foo = foo.sort_values(by="keys")

                reformatted_fill_best_response_for_col = []
                for jj in range(num_cols):
                    xxx = [x[jj] for x in fill_best_response_for_column]
                    reformatted_fill_best_response_for_col.append(xxx)

                best_response_for_col = []
                for pp in range(len(reformatted_fill_best_response_for_col)):
                    xxx = dotprod(reformatted_fill_best_response_for_col[pp],foo['prob'].tolist())
                    best_response_for_col.append(xxx)

                results_to_store_col = []
                results_to_store_col.append([k for k, m in enumerate(best_response_for_col) if m == max(best_response_for_col)])




                flat_list_column = [item for sublist in results_to_store_col for item in sublist]
                flat_list_row = [item for sublist in results_to_store_row for item in sublist]
                flat_list_row = list(set(flat_list_row))
                flat_list_column = list(set(flat_list_column))

                somelists = [flat_list_row,flat_list_column]
                cart_prod = [[a,b] for a in somelists[0] for b in somelists[1]]

  
                if len(cart_prod2[j]) > 1:
                    history_payoffs_aggregated = cart_prod2[j][1:]
                else:
                    history_payoffs_aggregated = [cart_prod2[j][0]]

  
                somelists = [[history_payoffs_aggregated[-1]],cart_prod]

                cart_prod2_intermediate = [[a,b] for a in somelists[0] for b in somelists[1]]

                if len(history_payoffs_aggregated) > 1:
                    cart_prod2_intermediate2 = [history_payoffs_aggregated[:-1] + i for i in cart_prod2_intermediate]
                else:
                    cart_prod2_intermediate2 = cart_prod2_intermediate

                tempcart1.append(cart_prod)

                tempcart2.append(cart_prod2_intermediate2)

            TimePeriodCart_prod_store.append(tempcart1)
            items2 = list(chain.from_iterable(tempcart2))
            cart_prod2 = items2



        flat_list_db = [item for sublist in TimePeriodCart_prod_store for item in sublist]
        flat_list_db2 = [item for sublist in flat_list_db for item in sublist]
        flat_list_db3 = [str(i) for i in flat_list_db2]
        cc = Counter(flat_list_db3)
        d=dict(cc)

 
        foo = pd.DataFrame([d],columns=d.keys()).T
        foo.columns = ["count"]
        foo = foo.sort_values(by="count",ascending=False)
        foo["keys"] = foo.index.tolist()
        foo["initial_history"] = str(tuple(history_payoffs))
        foo = foo.reset_index(drop=True)

        foo["count"] = foo["count"]/sum(foo["count"])
        foo["count"] = round(foo["count"]*100,2)


       
        foo["iteration_name"] = iteration_name
        foo["MemorySize"] = memory_length
        foo["TimePeriod"] = timeperiod
        foo["num_rows"] = num_rows
        foo["num_cols"] = num_cols
        foo["iterate_all"] = iterate_all
        ###

        foo.to_excel(path_to_save_output+"selected_iteration_payoffapproach_data_"+iteration_name+"_"+today+".xlsx",index=None)

    

        for uuu in range(len(TimePeriodCart_prod_store)):

            flat_list_db2_last = [item for sublist in TimePeriodCart_prod_store[uuu] for item in sublist]
            flat_list_db3_last = [str(i) for i in flat_list_db2_last]
            cc = Counter(flat_list_db3_last)
            d=dict(cc)
 
            foo_last = pd.DataFrame([d],columns=d.keys()).T
            foo_last.columns = ["count"]
            foo_last = foo_last.sort_values(by="count",ascending=False)
            foo_last["keys"] = foo_last.index.tolist()
            foo_last["initial_history"] = str(tuple(history_payoffs))
            foo_last["count1"] = foo_last["count"]/sum(foo_last["count"])
            foo_last["count1"] = round(foo_last["count1"]*100,2)
            foo_last = foo_last[["keys","initial_history","count1"]]
            foo_last["timeperiod"] = uuu
            trend_db_to_store = trend_db_to_store.append(foo_last,ignore_index=True)



        trend_db_to_store["iteration_name"] = iteration_name
        trend_db_to_store["MemorySize"] = memory_length
        trend_db_to_store["TimePeriod"] = timeperiod
        trend_db_to_store["num_rows"] = num_rows
        trend_db_to_store["num_cols"] = num_cols
        trend_db_to_store["iterate_all"] = iterate_all

        trend_db_to_store.to_excel(path_to_save_output+"selected_iteration_payoffapproach_data_timperiod_"+iteration_name+"_"+today+".xlsx",index=None)



        foorows = pd.DataFrame(empty_matrix_row)
        foocolumns = pd.DataFrame(empty_matrix_column)
        list_to_fill = []
        for i in range(num_rows):
            for j in range(num_cols):
                xxx = foorows.iloc[i][j]
                yyy = foocolumns.iloc[i][j]
                list_to_fill.append((xxx,yyy))


        emptypd_to_fill = foorows.copy()
        for i in range(num_rows):
            for j in range(num_cols):
                rowextract = np.array_split(list_to_fill,num_rows)[i].tolist()
                emptypd_to_fill.loc[i,j] = str(rowextract[j])



        emptypd_to_fill["iteration_name"] = iteration_name
        emptypd_to_fill["MemorySize"] = memory_length
        emptypd_to_fill["TimePeriod"] = timeperiod
        emptypd_to_fill["num_rows"] = num_rows
        emptypd_to_fill["num_cols"] = num_cols
        emptypd_to_fill["iterate_all"] = iterate_all

        emptypd_to_fill.to_excel(path_to_save_output+"selected_iteration_payoffapproach_data_payoffmatrix_"+iteration_name+"_"+today+".xlsx")

            
    
    if iterate_all == "YES":
        foo_to_fill = pd.DataFrame(columns=['count','keys','initial_history'])
        trend_db_to_store = pd.DataFrame(columns=["keys","initial_history","count1","timeperiod"])
        timelist = [lll for lll in range(timeperiod)]

        for zz in range(len(total_permutations)):
            for vv in range(memory_length):
                history_payoffs[vv] = total_permutations[zz][vv]

            TimePeriodCart_prod_store = []
            cart_prod2 = [history_payoffs]
            for t in range(timeperiod):
                tempcart1 = []
                tempcart2 = []

                for j in range(len(cart_prod2)):

                    distinct_elements_for_row = []
                    distinct_elements_for_column = []
                    for i in range(memory_length):
                        xx = cart_prod2[j][i][1]
                        distinct_elements_for_row.append(xx)
                        xx = cart_prod2[j][i][0]
                        distinct_elements_for_column.append(xx)
                    distinct_elements_for_row = list(set(distinct_elements_for_row))
                    distinct_elements_for_column = list(set(distinct_elements_for_column))


                    fill_best_response_for_row = []
                    for z in range(len(distinct_elements_for_row)):
                        temp_payoffs = []
                        for l in range(num_rows):
                            xx = empty_matrix_row[l,distinct_elements_for_row[z]]
                            temp_payoffs.append(xx)
                        fill_best_response_for_row.append(temp_payoffs)

                    probfreq_row = []
                    for kk in range(len(cart_prod2[j])):
                        foostorerow = cart_prod2[j][kk][1]
                        probfreq_row.append(foostorerow)


                    d = {x:probfreq_row.count(x) for x in probfreq_row}
                    foo = pd.DataFrame([d],columns=d.keys()).T
                    foo.columns = ["count"]
                    foo = foo.sort_values(by="count",ascending=False)
                    foo["keys"] = foo.index.tolist()
                    foo["prob"] = foo["count"]/memory_length
                    foo = foo.sort_values(by="keys")

                    reformatted_fill_best_response_for_row = []
                    for jj in range(num_rows):
                        xxx = [x[jj] for x in fill_best_response_for_row]
                        reformatted_fill_best_response_for_row.append(xxx)


                    best_response_for_row = []
                    for pp in range(len(reformatted_fill_best_response_for_row)):
                        xxx = dotprod(reformatted_fill_best_response_for_row[pp],foo['prob'].tolist())
                        best_response_for_row.append(xxx)


                    results_to_store_row = []
                    results_to_store_row.append([k for k, m in enumerate(best_response_for_row) if m == max(best_response_for_row)])


                    fill_best_response_for_column = []
                    for z in range(len(distinct_elements_for_column)):
                        temp_payoffs = []
                        for l in range(num_cols):
                            xx = empty_matrix_column[distinct_elements_for_column[z],l]
                            temp_payoffs.append(xx)
                        fill_best_response_for_column.append(temp_payoffs)


                    probfreq_col = []
                    for kk in range(len(cart_prod2[j])):
                        foostorecol = cart_prod2[j][kk][0]
                        probfreq_col.append(foostorecol)


                    d = {x:probfreq_col.count(x) for x in probfreq_col}
                    foo = pd.DataFrame([d],columns=d.keys()).T
                    foo.columns = ["count"]
                    foo = foo.sort_values(by="count",ascending=False)
                    foo["keys"] = foo.index.tolist()

                    foo["prob"] = foo["count"]/memory_length
                    foo = foo.sort_values(by="keys")

                    reformatted_fill_best_response_for_col = []
                    for jj in range(num_cols):
                        xxx = [x[jj] for x in fill_best_response_for_column]
                        reformatted_fill_best_response_for_col.append(xxx)

                    best_response_for_col = []
                    for pp in range(len(reformatted_fill_best_response_for_col)):
                        xxx = dotprod(reformatted_fill_best_response_for_col[pp],foo['prob'].tolist())
                        best_response_for_col.append(xxx)

                    results_to_store_col = []
                    results_to_store_col.append([k for k, m in enumerate(best_response_for_col) if m == max(best_response_for_col)])


                    flat_list_column = [item for sublist in results_to_store_col for item in sublist]
                    flat_list_row = [item for sublist in results_to_store_row for item in sublist]
                    flat_list_row = list(set(flat_list_row))
                    flat_list_column = list(set(flat_list_column))

                    somelists = [flat_list_row,flat_list_column]
                    cart_prod = [[a,b] for a in somelists[0] for b in somelists[1]]


                    if len(cart_prod2[j]) > 1:
                        history_payoffs_aggregated = cart_prod2[j][1:]
                    else:
                        history_payoffs_aggregated = [cart_prod2[j][0]]

                    somelists = [[history_payoffs_aggregated[-1]],cart_prod]
                    cart_prod2_intermediate = [[a,b] for a in somelists[0] for b in somelists[1]]

                    if len(history_payoffs_aggregated) > 1:
                        cart_prod2_intermediate2 = [history_payoffs_aggregated[:-1] + i for i in cart_prod2_intermediate]
                    else:
                        cart_prod2_intermediate2 = cart_prod2_intermediate


                    tempcart1.append(cart_prod)
                    tempcart2.append(cart_prod2_intermediate2)

                TimePeriodCart_prod_store.append(tempcart1)
                items2 = list(chain.from_iterable(tempcart2))
                cart_prod2 = items2


            flat_list_db = [item for sublist in TimePeriodCart_prod_store for item in sublist]
            flat_list_db2 = [item for sublist in flat_list_db for item in sublist]
            flat_list_db3 = [str(i) for i in flat_list_db2]
            cc = Counter(flat_list_db3)
            d=dict(cc)

            foo = pd.DataFrame([d],columns=d.keys()).T
            foo.columns = ["count"]
            foo = foo.sort_values(by="count",ascending=False)

            foo["keys"] = foo.index.tolist()
            foo["initial_history"] = str(total_permutations[zz])
            foo = foo.reset_index(drop=True)

            foo["count"] = foo["count"]/sum(foo["count"])
            foo["count"] = round(foo["count"]*100,2)

            foo_to_fill = foo_to_fill.append(foo,ignore_index=True)


            for uuu in range(len(TimePeriodCart_prod_store)):
                flat_list_db2_last = [item for sublist in TimePeriodCart_prod_store[uuu] for item in sublist]
                flat_list_db3_last = [str(i) for i in flat_list_db2_last]
                cc = Counter(flat_list_db3_last)
                d=dict(cc)

                foo_last = pd.DataFrame([d],columns=d.keys()).T
                foo_last.columns = ["count"]
                foo_last = foo_last.sort_values(by="count",ascending=False)
                foo_last["keys"] = foo_last.index.tolist()

                foo_last["initial_history"] = str(total_permutations[zz])
                foo_last = foo_last[["keys","count","initial_history"]]

                foo_last["count1"] = foo_last["count"]/sum(foo_last["count"])
                foo_last["count1"] = round(foo_last["count1"]*100,2)
                foo_last = foo_last[["keys","initial_history","count1"]]
                foo_last["timeperiod"] = uuu
                trend_db_to_store = trend_db_to_store.append(foo_last,ignore_index=True)



        foo_to_fill["iteration_name"] = iteration_name
        foo_to_fill["MemorySize"] = memory_length
        foo_to_fill["TimePeriod"] = timeperiod
        foo_to_fill["num_rows"] = num_rows
        foo_to_fill["num_cols"] = num_cols
        foo_to_fill["iterate_all"] = iterate_all

        foo_to_fill.to_excel(path_to_save_output+"all_iteration_payoffapproach_data_"+iteration_name+"_"+today+".xlsx",index=None)

        trend_db_to_store["iteration_name"] = iteration_name
        trend_db_to_store["MemorySize"] = memory_length
        trend_db_to_store["TimePeriod"] = timeperiod
        trend_db_to_store["num_rows"] = num_rows
        trend_db_to_store["num_cols"] = num_cols
        trend_db_to_store["iterate_all"] = iterate_all

        trend_db_to_store.to_excel(path_to_save_output+"all_iteration_payoffapproach_data_timperiod_"+iteration_name+"_"+today+".xlsx",index=None)


        foorows = pd.DataFrame(empty_matrix_row)
        foocolumns = pd.DataFrame(empty_matrix_column)
        list_to_fill = []
        for i in range(num_rows):
            for j in range(num_cols):
                xxx = foorows.iloc[i][j]
                yyy = foocolumns.iloc[i][j]
                list_to_fill.append((xxx,yyy))


        emptypd_to_fill = foorows.copy()
        for i in range(num_rows):
            for j in range(num_cols):
                rowextract = np.array_split(list_to_fill,num_rows)[i].tolist()
                emptypd_to_fill.loc[i,j] = str(rowextract[j])



        emptypd_to_fill["iteration_name"] = iteration_name
        emptypd_to_fill["MemorySize"] = memory_length
        emptypd_to_fill["TimePeriod"] = timeperiod
        emptypd_to_fill["num_rows"] = num_rows
        emptypd_to_fill["num_cols"] = num_cols
        emptypd_to_fill["iterate_all"] = iterate_all

        emptypd_to_fill.to_excel(path_to_save_output+"all_iteration_payoffapproach_data_payoffmatrix_"+iteration_name+"_"+today+".xlsx")


    return print("done")
