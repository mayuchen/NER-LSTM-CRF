

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
    sentence_origin = ''
    sentence_predict = ''
    flag = True
    for line in lines:
        line = line.rstrip('\n')
        if line == '':
            count += 1
            correct += 1 if flag else 0
            if not flag:
                print(sentence_origin)
                print(sentence_predict)
            flag = True
            sentence_origin = ''
            sentence_predict = ''
            continue
        segs = line.split('\t')
        if segs[3] != segs[4]:
            flag = False
        if segs[3].startswith('B'):
            sentence_origin += ('<%s>' % segs[3].split('-')[1])
        if segs[4].startswith('B'):
            sentence_predict += ('<%s>' % segs[4].split('-')[1])
        sentence_origin += segs[0]
        sentence_predict += segs[0]
        if segs[3].startswith('E'):
            sentence_origin += ('</%s>' % segs[3].split('-')[1])
        if segs[4].startswith('E'):
            sentence_predict += ('</%s>' % segs[4].split('-')[1])
    print(count)
    print(correct)
    print((0.0+correct)/count)


def data_clean(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
    lines = [line.replace('\r\n','').replace('\t\t\t', '') for line in lines]
    with open('data/315c.train','w') as fp:
        fp.writelines(lines)

if __name__ == '__main__':
    evaluate_slot('data/315c.result')
    # data_clean('data/315.train')
