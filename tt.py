import pickle

file = open("ckip_state", 'rb')
ckip_training_set_tf = pickle.load(file)
ckip_training_set_class = pickle.load(file)
ckip_seg_corpus = pickle.load(file)
file.close()


print(ckip_training_set_tf)
print(ckip_training_set_class)
print(ckip_seg_corpus)