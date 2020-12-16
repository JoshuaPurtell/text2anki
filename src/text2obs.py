
import jieba
import pandas as pd
###takes txt file and csvs of current repetoire and adds slides to the anki deck according to the set difference
###mostly for language acquisition use. 

###In order to not reinvent the wheel, and to integrate notes into a comprehensive language learning apparatus, we will be interfacing
###with obsidian.

###first, parse txt file to obsidian md

def txt_2_md(txt_path,csv_path,obsidian_folder_path,shingle_sizes,word_split):
    
    #open text
    txt_file=open(txt_path,mode='r')
    text=txt_file.read()

    #init md
    filename_base=(txt_path.split('/'))[-1].split('.')[0]
    with open(obsidian_folder_path + '/' + filename_base + '.md','w') as f:
        f.write(text)
    
    #now, parse the text by shingle length
    if (word_split==""):
        txt_by_word=[char for char in text]
    else:
        txt_by_word=text.split(word_split)
    print(txt_by_word)
    #test=[]

    #init flashcard list
    added_flashcard_list=[]

    #removing punctuation should be unnecessary
    for shingle in shingle_sizes:
        #have to use all shifts 
        #of the shingle
        for i in range(0,shingle):
            #now define the list of shingles
            num_whole_shingles=int((len(txt_by_word)-i)//shingle)
            middle=[word_split.join(txt_by_word[(i+j*shingle):(i+(j+1)*shingle)]) for j in range(num_whole_shingles)] #list comp for all but last
            #add first and last
            if (i>0):
                beginning=[word_split.join(txt_by_word[0:(i)])]
            else: 
                beginning=[]
            if (((len(txt_by_word)-i)%shingle==0)):
                end=[]
            else:
                end=[word_split.join(txt_by_word[(i+(num_whole_shingles)*shingle):len(txt_by_word)])]
            
            shingles=[*beginning,*middle,*end]

            #now check if any shingles are valid words
            valid_shingles=[]



#use jieba to partition words, then generate list to study. No automatic dictionary interface yet

def generate_md(txt_path,csv_path,obsidian_folder_path):
    #open text
    txt_file=open(txt_path,mode='r')
    text=txt_file.read()

    #init md
    filename_base=(txt_path.split('/'))[-1].split('.')[0]
    with open(obsidian_folder_path + '/' + filename_base + '.md','w') as f:
        print(text)
        f.write(text)
    
    #ok, now parse with jieba
    #should we first cut by punctuation?
    words=("/ ".join(jieba.cut(text,cut_all=False))).split("/")
    
    #clean it out
    dirty=[' ，',' 。']
    words_clean=list(set(words)-set(dirty))
    #print(set(words).intersection(set(dirty)))

    #pull in csv and compare
    try:
        current_repetoire=pd.read_csv(csv_path)
        new_words=[]
        for word in words_clean:
            if word in current_repetoire["word"].to_list():
                pass
            else:
                new_words.append(word)
    
    except IOError:
        current_repetoire=pd.DataFrame(data={'row': [i for i in range(len(words_clean))],'word': words_clean})
        new_words=words_clean
    
    #add new words to csv and save
    for nw in new_words:
        #current_repetoire.append(pd.DataFrame(data={'word':  nw}),ignore_index=True)
        current_repetoire.loc[len(current_repetoire.index)]=[len(current_repetoire.index),nw]
    #print(current_repetoire)
    current_repetoire.to_csv(csv_path,index=False)

    #use new words to form flash card section at end of md
    #construct flashcard section
    flashcards =[ 'Q: '+ nw + '\n' + 'A: ' for nw in new_words]
    #print(flashcards)
    #print(new_words)
    flashcard_section = ("\n\n").join(flashcards)

    with open(obsidian_folder_path + '/' + filename_base + '.md','r') as f:
        content_section=f.read()
    #print(content_section)
    #print(flashcard_section)
    with open(obsidian_folder_path + '/' + filename_base + '.md','w') as f:
        total_section = ("\n").join([text,"## New Vocabulary",flashcard_section,""])
        print(total_section)
        #print(text)
        #print(flashcard_section)
        f.write(total_section)

def send_completed_md_2_anki():
    pass

    

    

if __name__ == "__main__":
    txt_2_md_args=['/Users/AnR/documents/github/text2anki/example/articles/BAIDUtext.txt','/Users/AnR/documents/github/text2anki/example/example.csv','/Users/AnR/documents/languages/chinese/chinese_articles']
    generate_md(txt_2_md_args[0],txt_2_md_args[1],txt_2_md_args[2])



