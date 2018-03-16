import os
from lxml import etree
from sklearn.cross_validation import train_test_split
from jieba import posseg as pseg
import re
import jieba


SLOT_NAME = {'song': 'music.play', 'singer': 'music.play', 'theme': 'music.play', 'style': 'music.play', 'age': 'music.play',
             'toplist': 'music.play', 'emotion': 'music.play', 'language': 'music.play', 'instrument': 'music.play',
             'scene': 'music.play', 'destination': 'navigation.navigation', 'custom_destination': 'navigation.navigation',
             'origin': 'navigation.navigation', 'phone_num': 'phone_call.make_a_phone_call','contact_name': 'phone_call.make_a_phone_call'}

def load_dic(dirpath):
    slot_dic = {}
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        tag = filename.split('.')[0].replace(' ', '_')
        with open(filepath) as fp:
            for line in fp.readlines():
                slot_dic[line.rstrip('\n')] = tag
    return slot_dic

def load_data():
    with open('data/corpus.train.txt') as fp:
        lines = fp.readlines()
        lines = [line for line in lines if len(line) > 5]
        fp.close()
    train, test = train_test_split(lines, test_size=0.2)
    with open('data/corpus1.train','w') as fp:
        fp.writelines(train)
        fp.close()
    with open('data/corpus1.test', 'w') as fp:
        fp.writelines(test)
        fp.close()


def load_slot_data():
    with open('data/corpus.train.txt') as fp:
        sessions = fp.read().split('\n\n')
    train,test = train_test_split(sessions, test_size=0.2)
    with open('data/corpus_slot.train', 'w') as fp:
        fp.write('\n\n'.join(train))
        fp.close()
    with open('data/corpus_slot.test', 'w') as fp:
        fp.write('\n\n'.join(test))
        fp.close()
# def result_process

def LSTM_preprocess(sentence_o, sentence_t, fp):
    segs = pseg.cut(sentence_o)
    ENR = []
    s_label = []
    for word,f in segs:
        for ch in word:
            ENR.append(f)
    for key in SLOT_NAME.keys():
        s_tag = '<%s>' % key
        e_tag = '</%s>' % key
        sentence_t = sentence_t.replace(s_tag, '</o>'+s_tag)
        sentence_t = sentence_t.replace(e_tag, e_tag+'<o>')
    sentence_t = '<root><o>%s</o></root>' % sentence_t
    root = etree.fromstring(sentence_t)
    for node in root:
        content = node.text
        label = node.tag
        if not content:
            continue
        content = content.split('||')[0]
        for i in range(0, len(content)):
            if label == 'o':
                s_label.append('O')
            else:
                pos = 'B' if i == 0 else ('E' if i == len(content)-1 else 'I')
                s_label.append(pos + '-' + label)
    for i in range(0,len(sentence_o)):
        fp.write('%s\t%s\t%s\n' % (sentence_o[i],ENR[i],s_label[i]))
    fp.write('\n')


    # j = 0
    # tag = "O"
    # for i in range(0,len(sentence_o)):
    #     if sentence_o[i] == sentence_t[j]:
    #         print(tag)
    #     elif sentence_t[j] == '<':
    #         j += 1
    #         if sentence_t == '/':
    #
    #         tag = sentence_t[j]
    #         while sentence_t[j]!=

def LSTM_preprocess_session(session, fp):
    sentence_os = []
    sentence_ts = []
    for line in session.split('\n'):
        segs = line.split('\t')
        if len(segs) < 4:
            continue
        sentence_os.append(segs[1])
        sentence_ts.append(segs[3])
    LSTM_preprocess(' '.join(sentence_os), ' '.join(sentence_ts), fp)



if __name__ == '__main__':
    # slot_dic = load_dic('slot-dictionaries')
    # for word in slot_dic.keys():
    #     tag = slot_dic.get(word, 'udf')
    #     jieba.add_word(word, tag=tag)
    # load_slot_data()
    dataset_name = '316'
    fp = open('data/%s.test' % dataset_name, 'w')
    with open('data/corpus_slot.test') as fr:
        sessions = fr.read().split('\n\n')
        [LSTM_preprocess_session(session, fp) for session in sessions]
    fp = open('data/%s.train' % dataset_name, 'w')
    with open('data/corpus_slot.train') as fr:
        sessions = fr.read().split('\n\n')
        [LSTM_preprocess_session(session, fp) for session in sessions]

    # with open('data/corpus_slot.test') as fr:
    #     lines = fr.readlines()
    #     for line in lines:
    #         segs = line.split('\t')
    #         try:
    #             LSTM_preprocess(segs[1],segs[3],fp)
    #         except Exception as e:
    #             print(e)
    #             print(segs[3])
    # fp = open('data/%s.train','w')
    # with open('data/corpus.train') as fr:
    #     lines = fr.readlines()
    #     for line in lines:
    #         segs = line.split('\t')
    #         try:
    #             LSTM_preprocess(segs[1],segs[3],fp)
    #         except Exception as e:
    #             print(e)
    #             print(segs[3])
