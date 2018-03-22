
def sentence_serial(sentence, ch, tag_last, label):
    if tag_last == 'O' == label:
        sentence += ch
        return sentence, label
    if '-' not in label:
        sentence += '</%s>%s' % (tag_last, ch)
        return sentence, label
    try:
        [p_tag, tag] = label.split('-')
    except:
        import pdb
        pdb.set_trace()
    if tag_last == 'O':
        sentence += '<%s>%s' % (tag, ch)
        return sentence, tag
    if tag == tag_last and p_tag != 'B':
        sentence += '%s' % ch
        return sentence, tag
    sentence += '</%s><%s>%s' % (tag_last, tag, ch)
    return sentence, tag

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
    tag_o = 'O'
    tag_p = 'O'
    for idx, line in enumerate(lines):
        if sentence_origin == '':
            segs = line.rstrip('\n').split('\t')
            intent_o = segs[-2]
            intent_p = segs[-1]
            intent_flag = (intent_p == intent_o)
            # flag = intent_flag
            sentence_origin += 'intent: %s ' % intent_o
            sentence_predict += 'intent: %s ' % intent_p
            continue
        line = line.rstrip('\n')
        if line == '':
            sentence_origin, tag_o = sentence_serial(sentence_origin, '', tag_o, 'O')
            sentence_predict, tag_p = sentence_serial(sentence_predict, '',tag_p, 'O')
            count += 1
            # flag = flag or ('取消' in sentence_origin) or ('关闭' in sentence_origin)
            # intent_flag = intent_flag or ('取消' in sentence_origin) or ('关闭' in sentence_origin)
            correct += 1 if flag else 0
            intent_correct += 1 if intent_flag else 0
            if not flag:
                print(idx)
                print(sentence_origin)
                print(sentence_predict)
            flag = True
            sentence_origin = ''
            sentence_predict = ''
            continue
        segs = line.split('\t')
        if segs[-1] != segs[-2]:
            flag = False
        sentence_origin, tag_o = sentence_serial(sentence_origin, segs[0], tag_o, segs[-2])
        sentence_predict, tag_p = sentence_serial(sentence_predict, segs[0], tag_p, segs[-1])
    print(count)
    print(correct)
    print(intent_correct)
    print(correct/count)
    print(intent_correct/count)

def data_clean(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
    lines = [line.replace('\r\n', '').replace('\t\t\t', '') for line in lines]
    with open('data/315c.train', 'w') as fp:
        fp.writelines(lines)

if __name__ == '__main__':
    evaluate_slot('data/322.result')
    # evaluate_slot('data/crf/nohup.out')
    # data_clean('data/315.train')
