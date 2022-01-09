%Read the xlsx file with word counts
MText = readmatrix('Basel_I_Text_Data.xlsx');
MAlgo = readmatrix('Basel_I_Algo_Data.xlsx');

nText = size(MText);
nText = nText(1);
nAlgo = size(MAlgo);
nAlgo = nAlgo(1);

%Count matrix, 20 x 8 with:
%1: Unique Operands
%2: Unique Mathematical Operators
%3: Unique Logical Operators
%4: Unique Regulatory Operators
%5: Total Operands
%6: Total Mathematical Operators
%7: Total Logical Operators
%8: Total Regulatory Operators

MCountText = zeros(20,8);
MCountAlgo = zeros(20,8);

%Iterate over 20 regulations (last one being the total)
for i=1:20
    
    %Iterate over 4 "unique" measures
    for j=1:4
    
        %Iterate over all words
        for k=1:nText
        MCountText(i,j) = MCountText(i,j) + min(MText(k,i+5),1)*MText(k,j+1);
        end
        
        for k=1:nAlgo
        MCountAlgo(i,j) = MCountAlgo(i,j) + min(MAlgo(k,i+5),1)*MAlgo(k,j+1);
        end
        
    end
    
    %Iterate over 4 "total" measures
    for j=5:8
            
        %Iterate over 96 words
        for k=1:nText
        MCountText(i,j) = MCountText(i,j) + MText(k,i+5)*MText(k,j-4+1);
        end
        
        for k=1:nAlgo
        MCountAlgo(i,j) = MCountAlgo(i,j) + MAlgo(k,i+5)*MAlgo(k,j-4+1);
        end     
    end

end

%We now produce a 20 x 5 matrix with the following measures:
%1: Length
%2: Cyclomatic complexity
%3: Potential volume
%4: Operator diversity
%5: Level

MeasuresText = zeros(20,5);
MeasuresAlgo = zeros(20,5);

%Iterating over 20 regulations
for i=1:20
MeasuresText(i,1) = sum(MCountText(i,5:8));
MeasuresText(i,2) = MCountText(i,7);
MeasuresText(i,3) = 2 + MCountText(i,1);
MeasuresText(i,4) = sum(MCountText(i,2:4));
MeasuresText(i,5) = MeasuresText(i,3)/MeasuresText(i,1);
MeasuresAlgo(i,1) = sum(MCountAlgo(i,5:8));
MeasuresAlgo(i,2) = MCountAlgo(i,7);
MeasuresAlgo(i,3) = 2 + MCountAlgo(i,1);
MeasuresAlgo(i,4) = sum(MCountAlgo(i,2:4));
MeasuresAlgo(i,5) = MeasuresAlgo(i,3)/MeasuresAlgo(i,1);
end

Correlation_Table_Text = corr(MeasuresText(1:19,1:5));
Correlation_Table_Text = round(Correlation_Table_Text,2);
Correlation_Table_Text = array2table(Correlation_Table_Text,'VariableNames',{'Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
Correlation_Table_Algo = corr(MeasuresAlgo(1:19,1:5));
Correlation_Table_Algo = round(Correlation_Table_Algo,2);
Correlation_Table_Algo = array2table(Correlation_Table_Algo,'VariableNames',{'Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
table2latex(Correlation_Table_Text,'Correlation_Table_Text.tex')
table2latex(Correlation_Table_Algo,'Correlation_Table_Algo.tex')

Correlation_Table_Text_Spearman = corr(MeasuresText(1:19,1:5),'Type','Spearman');
Correlation_Table_Text_Spearman = round(Correlation_Table_Text_Spearman,2);
Correlation_Table_Text_Spearman = array2table(Correlation_Table_Text_Spearman,'VariableNames',{'Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
Correlation_Table_Algo_Spearman = corr(MeasuresAlgo(1:19,1:5),'Type','Spearman');
Correlation_Table_Algo_Spearman = round(Correlation_Table_Algo_Spearman,2);
Correlation_Table_Algo_Spearman = array2table(Correlation_Table_Algo_Spearman,'VariableNames',{'Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
table2latex(Correlation_Table_Text_Spearman,'Correlation_Table_Text_Spearman.tex')
table2latex(Correlation_Table_Algo_Spearman,'Correlation_Table_Algo_Spearman.tex')

%Table with correlations between algo-based and text-based measures.
%1st Column is Pearson correlation and 2nd column Spearman
Measures_Corr = zeros(5,2);
for i=1:5
Measures_Corr(i,1) = corr(MeasuresText(1:19,i),MeasuresAlgo(1:19,i));
Measures_Corr(i,2) = corr(MeasuresText(1:19,i),MeasuresAlgo(1:19,i),'Type','Spearman');
end

Measures_Corr_Table = round(Measures_Corr,2);
Measures_Corr_Table = array2table(Measures_Corr_Table);
table2latex(Measures_Corr_Table,'Measures_Corr.tex')

T=1:1:20;

%Save Table with measures.
MeasuresText = [T' MeasuresText];
MeasuresAlgo = [T' MeasuresAlgo];
Measures_Table_Text = round(MeasuresText,2);
Measures_Table_Text = array2table(Measures_Table_Text,'VariableNames',{'Regulation','Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
table2latex(Measures_Table_Text,'Measures_Table_Text.tex')
Measures_Table_Algo = round(MeasuresAlgo,2);
Measures_Table_Algo = array2table(Measures_Table_Algo,'VariableNames',{'Regulation','Length','Cyclomatic','Potential Volume','Operator Diversity','Level'});
table2latex(Measures_Table_Algo,'Measures_Table_Algo.tex')