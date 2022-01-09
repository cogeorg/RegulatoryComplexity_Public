%Read the xlsx file with word counts
M = readmatrix('random_regulations_data.xlsx');
M = M(2:end,:);
nText = size(M);
nText = nText(1);

%Count matrix, 41 x 8 with:
%1: Unique Operands
%2: Unique Mathematical Operators
%3: Unique Logical Operators
%4: Unique Regulatory Operators
%5: Total Operands
%6: Total Mathematical Operators
%7: Total Logical Operators
%8: Total Regulatory Operators

MCount = zeros(41,8);

%Iterate over 41 regulations (last one being the total)
for i=1:41
    
    %Iterate over 4 "unique" measures
    for j=1:4
    
        %Iterate over all words
        for k=1:nText
        MCount(i,j) = MCount(i,j) + min(M(k,i+5),1)*M(k,j+1);
        end
       
        
    end
    
    %Iterate over 4 "total" measures
    for j=5:8
            
        %Iterate over 96 words
        for k=1:nText
        MCount(i,j) = MCount(i,j) + M(k,i+5)*M(k,j-4+1);
        end
        
    end

end

%We now produce a 41 x 6 matrix with the following measures:
%1: Length
%2: Cyclomatic complexity
%3: Quantity of regulations
%4: Potential volume
%5: Operator diversity
%6: Level

MeasuresText = zeros(41,6);

%Iterating over 41 regulations
for i=1:41
MeasuresText(i,1) = sum(MCount(i,5:8));
MeasuresText(i,2) = MCount(i,7);
MeasuresText(i,3) = MCount(i,8);
MeasuresText(i,4) = 2 + MCount(i,1);
MeasuresText(i,5) = sum(MCount(i,2:4));
MeasuresText(i,6) = MeasuresText(i,4)/MeasuresText(i,1);
end

%The 38 regulations we are using correspond to lines 2 to 39.
Correlation_Table_Text = corr(MeasuresText(2:39,1:6));
Correlation_Table_Text = round(Correlation_Table_Text,2);
Correlation_Table_Text = array2table(Correlation_Table_Text,'VariableNames',{'Length','Cyclomatic','Quantity','Potential Volume','Operator Diversity','Level'});
table2latex(Correlation_Table_Text,'Correlation_Table_Text.tex')

Correlation_Table_Text_Spearman = corr(MeasuresText(2:39,1:6),'Type','Spearman');
Correlation_Table_Text_Spearman = round(Correlation_Table_Text_Spearman,2);
Correlation_Table_Text_Spearman = array2table(Correlation_Table_Text_Spearman,'VariableNames',{'Length','Cyclomatic','Quantity','Potential Volume','Operator Diversity','Level'});
table2latex(Correlation_Table_Text_Spearman,'Correlation_Table_Text_Spearman.tex')

%Save Table with measures.
T=0:1:40;
MeasuresText = [T' MeasuresText];
Measures_Table_Text = round(MeasuresText,2);
Measures_Table_Text = array2table(Measures_Table_Text,'VariableNames',{'Regulation','Length','Cyclomatic','Quantity','Potential Volume','Operator Diversity','Level'});
table2latex(Measures_Table_Text,'Measures_Table_Text.tex')

writetable(Measures_Table_Text,'Measures.csv') 
