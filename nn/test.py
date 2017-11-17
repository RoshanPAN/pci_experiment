import numpy as np
import tensorflow as tf
from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

a = np.load("01_normal_Nov10_labeled.numpy")
b = np.load("03_with_memory_fill_Nov11_part1_labeled.numpy")
c = np.load("03_with_memory_fill_Nov11_part2_labeled.numpy")
d = np.load("03_with_memory_fill_Nov11_part3_labeled.numpy")
e = np.load("03_with_memory_fill_Nov11_part4_labeled.numpy")
f = np.load("05_with_network_partition_part1_labeled.numpy")
n = np.load("05_with_network_partition_part2_labeled.numpy")

all_data = np.concatenate((b,c,d,e,f,n))

features = all_data[:,0:243]
features_scaled = preprocessing.scale(features)

labels = all_data[:,243].astype(int).reshape(-1)
print("0:",np.sum(labels==0))
print("1:",np.sum(labels==1))
print("2:",np.sum(labels==2))


one_hot_labels = np.eye(3)[labels]



features_scaled_random,one_hot_labels_random = shuffle(features_scaled,one_hot_labels)
X_train, X_validation, y_train, y_validation = train_test_split(features_scaled_random, one_hot_labels_random, test_size=0.20, random_state=42)
#print("Old X_train size:",len(features_scaled_random))
#print("New X_train size:",len(X_train))
#print("X_validation size:",len(X_validation))


input_data = tf.placeholder(tf.float32, shape=[None,243])
target_data = tf.placeholder(tf.float32, shape=[None,3])

hidden_nodes = 81

input_weights = tf.Variable(tf.truncated_normal([243,hidden_nodes]))
input_biases = tf.Variable(tf.zeros([hidden_nodes]))

hidden_weights = tf.Variable(tf.truncated_normal([hidden_nodes,3]))
hidden_biases = tf.Variable(tf.zeros([3]))

input_layer = tf.matmul(input_data, input_weights)
hidden_layer = tf.nn.relu(input_layer + input_biases)
digit_label = tf.matmul(hidden_layer, hidden_weights) + hidden_biases

loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=digit_label, labels=target_data))
optimizer = tf.train.GradientDescentOptimizer(0.009).minimize(loss_function)

correct_prediction = tf.equal(tf.argmax(digit_label,1), tf.argmax(target_data,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

EPOCHS = 2000
BATCH_SIZE = 128
num_examples = len(X_train)
print (num_examples)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

for x in range(EPOCHS):
	X_train,y_train = shuffle(X_train,y_train)
	for offset in range(0,num_examples,BATCH_SIZE):
		batch_x, batch_y = X_train[offset:offset+BATCH_SIZE], y_train[offset:offset+BATCH_SIZE]
		optimizer.run(feed_dict={input_data: batch_x, target_data: batch_y})
	if ((x+1) % 100 == 0):
		print("Training epoch " + str(x+1))
		print("Accuracy: " + str(accuracy.eval(feed_dict={input_data: X_validation, target_data: y_validation})))




