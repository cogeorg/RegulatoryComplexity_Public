#!/usr/bin/env python
# coding: utf-8

# # download from Github and content extraction

# In[14]:


# list of functions

# extract .txt file names
def extract_txt_file_names(data):
    # Extract all the txt.files names
    txt_files = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'items' and isinstance(value, list):
                for item in value:
                    if item.get('contentType') == 'file' and item.get('name').endswith('.txt'):
                        file_name = item.get('name')
                        txt_files.append(file_name)
            else:
                txt_files.extend(extract_txt_file_names(value))
    return txt_files


# extract txt files content
def extract_content(txt_file_names):
    base_url = "https://raw.githubusercontent.com/cogeorg/RegulatoryComplexity_Public/main/010_cleaned_data/DoddFrank/Sections/"

    contents=[]
    for i in trange(len(txt_file_names)):
        file_url = base_url + txt_file_names[i]
        content= ' '.join(requests.get(file_url).content.decode('utf-8').replace('\n', ' ').split())
        contents.append(content)
    return contents    





# # sentence wise 

# In[1]:


# split each text into sentences
def split_into_sentences(text):
    # Regular expression for splitting into sentences
    sentence_splitter = re.compile(r'(?<=\S\.)\s')
    return sentence_splitter.split(text)

# preprocess the text by removing punctuation, convert to lower case and apply pos tag and lemmatization
def preprocessing(sentences):
    preprocessed_sentences = []
    for sentence in sentences:
        # tokenize and assign pos_tag
        tokens = pos_tag(word_tokenize(sentence))
        
        # lemmatize and convert to lower case
        lemmatizer = WordNetLemmatizer()
        tokens=[(lemmatizer.lemmatize(word.lower()), tag) for word, tag in tokens]
        
        # Remove specific tokens
        stop_words=['gt','lt']
        tokens = [(word, tag) for word, tag in tokens if word not in stop_words]
      
        # remove punctuation
        punctuation = set(string.punctuation).union({'--', ':', ',', "''", '``', 'EN.  '})
        tokens = [(word, tag) for word, tag in tokens if word not in punctuation]

        preprocessed_sentences.append(tokens)

    return preprocessed_sentences

# find all possible ngrams of a specific length and that appear at least a given number of times
def get_ngrams_df(preprocessed_sentences, n, threshold):
    # Generate ngrams for each sentence
    all_ngrams = []
    for sentence in preprocessed_sentences:
        # Ensure the sentence length is at least n
        if len(sentence) >= n:
            sentence_ngrams = ngrams(sentence, n)
           # all_ngrams.extend(sentence_ngrams)
            all_ngrams.extend([ngram for ngram in sentence_ngrams if not any('*' in word for word, _ in ngram)])

    # Count frequencies of ngrams
    ngram_freq = Counter(all_ngrams)

    # Filter ngrams that meet the threshold
    frequent_ngrams = [(ngram, count) for ngram, count in ngram_freq.items() if count >= threshold]

    # Sort by most frequent
    frequent_ngrams.sort(key=lambda x: x[1], reverse=True)

    # Transform each ngram to the desired format
    frequent_ngrams_transformed = [{'Ngram': ngram, 'Count': count, 
                                    'Words': tuple(word for word, _ in ngram), 
                                    'POSTags': tuple(tag for _, tag in ngram)} 
                                   for ngram, count in frequent_ngrams]

    # Create DataFrame
    ngrams_df = pd.DataFrame(frequent_ngrams_transformed)

    # Check for duplicates and add filters
    word_set_counts = Counter(ngram['Words'] for ngram in frequent_ngrams_transformed)
    for ngram in ngrams_df.itertuples():
        ngrams_df.at[ngram.Index, 'Has_duplicates'] = 1 if word_set_counts[ngram.Words] > 1 else 0
        ngrams_df.at[ngram.Index, 'contain_digit'] = 1 if any(char.isdigit() for word in ngram.Words for char in word) else 0
        ngrams_df.at[ngram.Index, 'contain_single_letter'] = 1 if any(len(word) == 1 and word.isalpha() for word in ngram.Words) else 0
        ngrams_df.at[ngram.Index, 'Length'] = n

    # Drop the 'Ngram' column
    ngrams_df = ngrams_df.drop('Ngram', axis=1)

    # Reorder the columns
    ngrams_df = ngrams_df[['Words', 'POSTags', 'Length','Count', 'Has_duplicates', 'contain_digit', 'contain_single_letter']]

    return ngrams_df


# Convert ngram tuple to string
def ngram_to_string(ngram):
    return ' '.join(ngram)

# Find indices where ngram with specific tags occurs within sentences
def find_ngram_with_tags(sentences_words, sentences_tags, ngram_words, ngram_tags):
    n = len(ngram_words)
    indices = []
    for sentence_index, (sentence_words, sentence_tags) in enumerate(zip(sentences_words, sentences_tags)):
        for i in range(len(sentence_words) - n + 1):
            if sentence_words[i:i + n] == ngram_words and sentence_tags[i:i + n] == ngram_tags:
                indices.append(sentence_index)
    return indices

# Process each ngram with its tags considering the sentence structure (manipulation)
def process_ngram_with_tags(ngram, ngram_tags, texts, tags, filenames):
    ngram_words = ngram_to_string(ngram).split()
    ngram_tags = ngram_to_string(ngram_tags).split()
    all_occurrences = [(text, find_ngram_with_tags(text, tag, ngram_words, ngram_tags), filename) 
                       for text, tag, filename in zip(texts, tags, filenames)]

    # Flatten occurrences and sample up to 3 unique sentences
    all_sentences_with_ngram = [(text_sentences[index], filename) 
                                for text_sentences, indices, filename in all_occurrences 
                                for index in indices]
    
    random.shuffle(all_sentences_with_ngram)
    sampled_sentences = random.sample(all_sentences_with_ngram, min(3, len(all_sentences_with_ngram)))

   # occurrence_counts = sum(len(indices) for _, indices, _ in all_occurrences)
    contexts, context_filenames = zip(*sampled_sentences) if sampled_sentences else ([], [])
    #occurrence_counts
    return [' '.join(sentence) for sentence in contexts], list(context_filenames)


# remove ngrams from the text
def remove_ngrams_from_text(ngrams_df, df, source_text='preprocessed_text'):
    # Check if 'ngram_removal_text' column exists and adjust source_text accordingly
    if 'ngram_removal_text' in df.columns:
        source_text = 'ngram_removal_text'
    
    # Extract ngrams and convert from tokenized version into string
    ngram_strings = [' '.join(token) for token in ngrams_df['Words'].tolist()]
    ngram_tags = [' '.join(token) for token in ngrams_df['POSTags'].tolist()]

    # Convert text from tokenized version into string while maintaining the original grouping
    text_strings = []
    text_tags = []
    for i in range(len(df)):
        # Collect all sentences and tags for the current row into separate lists
        sentences = [' '.join(token) for token in df[source_text][i]]
        tags = [' '.join(token) for token in df['preprocessed_tags'][i]]
        # Append these lists to text_strings and text_tags, preserving the row-wise grouping
        text_strings.append(sentences)
        text_tags.append(tags)

    # Iterate over each text string and its corresponding tags to substitute ngrams with '*'
    for i in range(len(text_strings)):
        for j, (sentence, tags) in enumerate(zip(text_strings[i], text_tags[i])):
            modified_sentence = sentence  # Initialize modified sentence
            for k, ngram in enumerate(ngram_strings):
                ngram_tag = ngram_tags[k]
                if ngram in modified_sentence and ngram_tag in tags:
                    # Create the replacement string
                    replacement = ' '.join(['*' for _ in ngram.split()])
                    # Replace the ngram in the modified sentence with the replacement string
                    modified_sentence = modified_sentence.replace(ngram, replacement)
            # Update the sentence in text_strings with the modified sentence
            text_strings[i][j] = modified_sentence

    # Combine the processed words and tags back into the desired format
    text_strings_tag = [[[(word, tag) for word, tag in zip(sentence.split(), tags.split())] for sentence, tags in zip(paragraph, tag_paragraph)] for paragraph, tag_paragraph in zip(text_strings, text_tags)]

    # Update the DataFrame in-place
    df['ngram_removal'] = text_strings_tag
    df['ngram_removal_text'] = [[[word for word, _ in sentence] for sentence in row] for row in df['ngram_removal']]

    return df

# import validated excel file and manipulate them to prepare for next iteration
def process_ngrams_file(filepath):
    # Read the data
    df = pd.read_excel(filepath)
    
    # Filter the DataFrame
    df = df[df['include'] == 1]
    
    # Drop unnecessary columns
    df = df.drop(columns=['include', 'is_in_dictionary'])
    
    # Convert string representations of lists back into actual lists
    for column in ['Words', 'POSTags', 'Random_Examples', 'Example_Filenames']:
        df[column] = df[column].apply(ast.literal_eval)
    
    return df


# apply the ngram search and removal iteratively till n=2 included.
def get_ngrams_iteration(df, n, threshold, final_ngrams_df):
    i = n  # Start from n
    if i < 4:
        threshold = 2*threshold
    while i >= 2:  # Ensure i doesn't go below 2
        # Flatten the list of sentences into a single list for n-gram processing
        flattened_sentences = [word_tag for sentence in df['ngram_removal'] for word_tag in sentence]
        try:
            ngrams_df = get_ngrams_df(flattened_sentences, n=i, threshold=threshold)
            
            print(f'There are {len(ngrams_df)} n-grams of length {i}, of which {len(ngrams_df[ngrams_df["Has_duplicates"] == 1])} are duplicates')

            # Add the examples variable
            ngrams_df['Random_Examples'], ngrams_df['Example_Filenames'] = zip(*ngrams_df.progress_apply(lambda row: process_ngram_with_tags(row['Words'], row['POSTags'], df['preprocessed_text'].tolist(), df['preprocessed_tags'].tolist(), df['filename'].tolist()), axis=1))

            final_ngrams_df = pd.concat([final_ngrams_df, ngrams_df])

            # Remove ngrams
            df = remove_ngrams_from_text(ngrams_df, df,source_text='ngram_removal_text')
           
            i -= 1  
        except Exception as e:
            print(str(i)+' length not found')
            i -= 1  

    return df, final_ngrams_df



# remove ngrams iteratively
def remove_text(patterns, df, source_text='final_text'):
    # Initialize the final_text_removed column with NaN
    df['final_text_removed'] = np.nan
    # Compile patterns into regular expressions that match whole words, with optional punctuation at the boundaries
    regex_patterns = [re.compile(r'\b' + re.escape(pattern) + r'\b[\.\,]?', re.IGNORECASE) for pattern in patterns]

    for i in trange(len(df)):
        text = df[source_text][i]
        modified_text = text  # Initialize modified text
        for pattern in regex_patterns:
            # Replace the ngram in the modified text with the replacement string
            modified_text = pattern.sub(lambda x: ' '.join(['*' for _ in x.group().split()]), modified_text)
        # Update the text in the DataFrame with the modified text
        df.loc[i, 'final_text_removed'] = modified_text

    return df


# get the list of the remaining words after the remove_text function was applied
def get_remaining_words(df, column='final_text_removed'):
    # Create a set to store unique remaining words
    remaining_words = set()

    # Iterate over each row in the DataFrame
    for text in df[column]:
        # Split the text into words
        words = text.split()
        # Update the set with words that do not contain '*' and are not punctuation, stripping punctuation from ends
        remaining_words.update(
            word.strip(string.punctuation) for word in words 
            if '*' not in word and not all(char in string.punctuation for char in word)
        )

    # Convert the set to a list and return
    return list(remaining_words)


# In[ ]:




