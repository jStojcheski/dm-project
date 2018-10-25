# set working directory
setwd('E:/R_projects/DM_project/')

# read & remove items without coefficient
data_in = read.csv(file = 'data/Spenser_1_8_new_format_on_PE_markers.tsv', sep = '\t')
data_in = data_in[!is.na(data_in$SAPECoeficient) | !is.na(data_in$APECoeficient), ]
row.names(data_in) = 1:length(row.names(data_in))

# get set of all employees
employees = as.vector(data_in$TERRID)
employees = sort(unique(employees))

empl_dict = vector(mode = 'list', length = length(employees))
names(empl_dict) = employees

# fill NA with 0
data_in[c('SAPECoeficient', 'APECoeficient')][is.na(data_in[c('SAPECoeficient', 'APECoeficient')])] <- 0

# merge SAPE and APE coefficient columns
data_in$maxRows = apply(data_in[c('SAPECoeficient', 'APECoeficient')], 1, max)


counter = 0
for (employee in employees) {
    empl_dict[[employee]] = c()
    empl_subset = data_in[data_in$TERRID == employee, ]
    customers = unique(as.vector(empl_subset$CustomerID))
    
    for (customer in customers) {
        # cat(sprintf("%s %s\n", employee, customers))
        cust_subset = empl_subset[empl_subset$CustomerID == customer, ]
        x = cust_subset$maxRows
        
        if (length(x) > 2) {
            for (i in 1:length(x)) {
                index = row.names(cust_subset)[i]
                
                temp = x[i]
                x[i] = NA
                
                data_in[index, 'interpolation'] = imputeTS::na.interpolation(x)[i]
                # data_in[index, 'kalman']        = imputeTS::na.kalman(x)[i]
                data_in[index, 'mov_avg']       = imputeTS::na.ma(x)[i]
                data_in[index, 'season_decomp'] = imputeTS::na.seadec(x)[i]
                data_in[index, 'season_split']  = imputeTS::na.seasplit(x)[i]
                
                y = data_in[index, 'interpolation']
                x[i] = temp
                diff = sum((x[i] - y) ** 2) * temp / 100
                # print(diff)
                empl_dict[[employee]] = append(empl_dict[[employee]], diff)
                
                counter = counter + 1
                cat(sprintf("%d/%d\n", counter, length(row.names(data_in))))
            }
        }
        else {
            counter = counter + length(x)
            cat(sprintf("%d/%d\n", counter, length(row.names(data_in))))
        }
    }
}

empl_df = data.frame(row.names = employees)
for (employee in employees) {
    ts_mse = mean(as.numeric(empl_dict[[employee]]))
    cat(sprintf("%s: %.4f\n", employee, ts_mse))
    empl_df[employee, 'ts_mse'] = ts_mse
}

write.csv(x = empl_df, file='data/ts_mse.csv')
write.csv(x = data_in, file='data/imputed_data.csv')