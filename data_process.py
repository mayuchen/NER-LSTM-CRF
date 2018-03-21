

def merge_feature(feature_file1, feature_file2, fw):
    fp1 = open(feature_file1)
    fp2 = open(feature_file2)
    lines1 = fp1.readlines()
    lines2 = fp2.readlines()

def evaluate_slot(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
    count = 0
    correct = 0
    intent_correct = 0
    sentence_origin = ''
    sentence_predict = ''
    flag = True
    intent_flag = True
    tag = 'O'
    for idx, line in enumerate(lines):
        if sentence_origin == '':
            segs = line.rstrip('\n').split('\t')
            intent_o = segs[-2]
            intent_p = segs[-1]
            intent_flag = (intent_p == intent_o)
            flag = intent_flag
            sentence_origin += 'intent:%s ' % intent_o
            sentence_predict += 'intent:%s ' % intent_p
            continue
        line = line.rstrip('\n')
        if line == '':
            count += 1
            correct += 1 if flag else 0
            intent_correct += 1 if intent_flag else 0
            if not flag:
                print(sentence_origin)
                print(sentence_predict)
            flag = True
            sentence_origin = ''
            sentence_predict = ''
            continue
        segs = line.split('\t')
        if segs[-1] != segs[-2]:
            flag = False
        if segs[-2].startswith('B'):
            sentence_origin += ('<%s>' % segs[-2].split('-')[1])
        if segs[-1].startswith('B'):
            sentence_predict += ('<%s>' % segs[-1].split('-')[1])
        sentence_origin += segs[0]
        sentence_predict += segs[0]
        if segs[-2].startswith('E'):
            sentence_origin += ('</%s>' % segs[-2].split('-')[1])
        if segs[-1].startswith('E'):
            sentence_predict += ('</%s>' % segs[-1].split('-')[1])
    print(count)
    print(correct)
    print(intent_correct)
    print(correct/count)
    print(intent_correct/count)

def data_clean(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
    lines = [line.replace('\r\n','').replace('\t\t\t', '') for line in lines]
    with open('data/315c.train','w') as fp:
        fp.writelines(lines)

if __name__ == '__main__':
    evaluate_slot('data/318.result')
    # evaluate_slot('data/crf/nohup.out')
    # data_clean('data/315.train')
