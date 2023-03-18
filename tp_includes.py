# functions
def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc))
             if word not in stop_words] for doc in texts]


def get_corpus_id2word(data):
    # convert data to words
    data_words = list(sent_to_words(data))

    # remove stop words
    data_words = remove_stopwords(data_words)

    idocs = []
    for doc in data_words:
        lemmed = [WordNetLemmatizer().lemmatize(w) for w in doc]
        #        stemmed = [PorterStemmer().stem(w) for w in doc]
        idocs.append(lemmed)
    #        idocs.append(stemmed)

    data_words = idocs

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)

    # Create Corpus
    texts = data_words

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    return corpus, id2word, idocs


stop_words = stopwords.words('english')
stop_words.extend(['data',
                   'driven',
                   'show',
                   'get',
                   'knowledge',
                   'yes'
                   'also',
                   'give',
                   'already',
                   'etc',
                   'also',
                   'based',
                   'approach',
                   'analytics',
                   'way',
                   'ensure',
                   'line',
                   'buttom',
                   'yes',
                   'would',
                   'thing',
                   'le',
                   'increase',
                   'use',
                   'using',
                   'make',
                   'made',
                   'definitely',
                   'one',
                   'maybe',
                   'something',
                   'people',
                   'new',
                   #                    'training',
                   'organisation',
                   'bmw',
                   'v',
                   'create',
                   'nan',
                   'session',
                   'could',
                   'better'
                   ])


def do_topic_model(int_df_text, int_i_stage, int_num_topics, int_i_random_state):
    # get data

    if len(int_i_stage) > 0:
        data = int_df_text[int_i_stage].values.tolist()
    #         print(data)
    else:
        data = int_df_text.values.tolist()

        # get corpus and id2words
    corpus, id2word, lemmed = get_corpus_id2word(data)

    # Build LDA model

    # SOME_FIXED_SEED = 42

    # # before training/inference:
    # np.random.seed(SOME_FIXED_SEED)

    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=int_num_topics,
                                           random_state=int_i_random_state)
    # print topics
    pprint(lda_model.print_topics())

    # Compute Perplexity
    print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=lemmed, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

    # save the Keyword in the 10 topics in topics
    topic = lda_model.show_topics(formatted=False)
    ifield = [int_i_stage, topic]
    topics.append(ifield)

    # Visualize the topics
    pyLDAvis.enable_notebook()
    LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_' + int_i_stage + '_' + str(int_num_topics))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = gensimvis.prepare(lda_model, corpus, id2word)

        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)

    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
    pyLDAvis.save_html(LDAvis_prepared,
                       './results/ldavis_prepared_' + int_i_stage + '_' + str(int_num_topics) + '.html')
    return LDAvis_prepared, topics


def visualize_topic_modeling(i_stage, i_topics, my_list):
    # populate dataframe with the weights
    ls_stage = []
    ls_topic = []
    ls_kword = []
    ls_weight = []

    # loop deur die stages, can change and improve this
    for stages in i_topics:
        if stages[0] == i_stage:
            for stage in stages[1]:
                for topic in stage[1]:
                    ls_stage.append(stages[0])
                    ls_topic.append(stage[0])
                    ls_kword.append(topic[0])
                    ls_weight.append(topic[1])

                    # initialise data of lists.
    data = {'Stage': ls_stage,
            'Topic': ls_topic,
            'Keyword': ls_kword,
            'Value': ls_weight}

    # Create DataFrame
    df = pd.DataFrame(data)

    df['Stage_topic'] = df['Stage'].astype(str).str[0] + df['Topic'].astype(str)

    ls_words = df['Keyword'].unique().tolist()
    ls_stage_topic = df['Stage_topic'].unique().tolist()

    # heatmap dataframe empty
    df_heatmap = pd.DataFrame(np.array(np.zeros(len(df['Keyword'].unique()))),
                              columns=['col1'],
                              index=ls_words)

    print(df_heatmap.shape)

    # populate heatmap
    for stage_topic in ls_stage_topic:

        ls_iweight = []
        for ikey in ls_words:

            ivalue = df['Value'][(df['Stage_topic'] == stage_topic) & (df['Keyword'] == ikey)].values
            if len(ivalue) == 1:
                iweight = ivalue[0]
            else:
                iweight = 0
                #         print(ikey, iweight)
            ls_iweight.append(iweight)

        df_heatmap[stage_topic] = ls_iweight
        df_heatmap

    df_heatmap = df_heatmap.drop(['col1'], axis=1)

    # remove words that are not adding value
    df_heatmap = df_heatmap[~df_heatmap.index.isin(my_list)]

    fig, ax = plt.subplots(figsize=(4, 5))  # Sample figsize in inches

    cmap = copy.copy(plt.get_cmap("Blues"))
    cmap.set_under('#FFFFFF')

    sns.color_palette("Blues", as_cmap=True)
    #     sns.heatmap(df_heatmap, linewidths=.5, ax=ax, cmap=cmap, cbar=False, vmin=1e-2, center=1e-100);
    sns.heatmap(df_heatmap, linewidths=.5, ax=ax, cmap=cmap, cbar=False, vmin=((1e-2) * 0.01), center=1e-300);