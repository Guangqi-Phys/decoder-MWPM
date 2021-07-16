import matplotlib.pyplot as plt
from tcfunctions import *



l_simult = [3,7,11] # matrix size to simulate
n_simult = 10000  # number of simulations 

# generating the parobability list
d_prob = 0.002
prob_start = 0.09
prob_end = 0.12
probs = []
for i in range(int((prob_end-prob_start)/d_prob+1.01)):
	probs.append(prob_start+d_prob*i)


# simulating

data = []
data_file = 'data.dat'
for l in l_simult:
	for prob in probs:
		accu_rate = 0
		for ind_n in range(n_simult):
			m_stablz, m_qubits = torus_initial(l, l)
			er_stablz, er_qubits = torus_error(m_stablz, m_qubits, prob)
			matching = mwpm_toric(er_stablz)
			crted_qubits = correct_qubits(matching,er_qubits)
			check_bool = check_logical(crted_qubits)
			accu_rate +=check_bool
		accu_rate = 1- accu_rate/n_simult
		data.append([l,prob,accu_rate])
		with open(data_file, 'w') as f:
			for d in data:
				f.write(' '.join([str(x) for x in d]))
				f.write('\n')






# plotting
data_trans = list(map(list, zip(*data)))
data_plot = []
data_plot.append(probs)
for i  in range(0,len(probs)*len(l_simult),len(probs)):
	data_plot.append(data_trans[2][i:i+len(probs)])

for i in range(len(l_simult)):
	plt.plot(data_plot[0],data_plot[i+1])

labels_list =[]
l_simult_str = [str(i) for i in l_simult]
for i in range(len(l_simult)):
	str1 = list(l_simult_str[i])
	str1.insert(0,'L = ')
	labels_list.append(''.join(str1))

plt.legend(labels= labels_list )
plt.axis([prob_start, prob_end, 0, 0.6])
plt.title(r'Toric Code - MWPM')
plt.xlabel(r'Qubit error rate')
plt.ylabel(r'Logical error rate')


plt.savefig('mwpm.pdf',dpi=600,format='pdf')
plt.show()









