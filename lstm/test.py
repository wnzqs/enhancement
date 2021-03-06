# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import numpy as np
from lstm import LstmParam, LstmNetwork
import matplotlib.pyplot as plt
# from lstm import lstm


class ToyLossLayer(object):
    """
    Computes square loss with first element of hidden layer array.
    """
    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2  # 误差函数  **=^
    # 一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
    # 而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff
    # 损失函数的导函数


def example_0():
    # learns to repeat simple sequence from random inputs
    np.random.seed(0)
    # 一般计算机的随机数都是伪随机数，以一个真随机数（种子）作为初始条件，然后用一定的算法不停迭代产生随机数

    # parameters for input data dimension and lstm cell count 
    mem_cell_ct = 7  # hidden 输出的维度
    x_dim = 50  # 输入变量维度
    lstm_param = LstmParam(mem_cell_ct, x_dim)  # 神经网络初始化 返回初始化的net对象
    lstm_net = LstmNetwork(lstm_param)
    y_list = [0.5, 0.2, 0.1, 0.5, 0.7]
    input_val_arr = [np.random.random(x_dim) for _ in y_list]
    loss = list()
    lstm_net.net_initial(y_list)

    for cur_iter in range(400):  # 迭代次数
        print("cur iter: ", cur_iter)
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])
            print("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.h[0]))

        loss.append(lstm_net.y_list_is(y_list, ToyLossLayer))  # 计算误差并且计算梯度
        print("loss: ", loss[cur_iter])
        lstm_param.apply_diff(lr=0.1)  # 梯度下降法 修正net
        lstm_net.x_list_clear()
    for ind in range(len(y_list)):
        print("y_pred[%d] : %f" % (ind, lstm_net.lstm_node_list[ind].state.h[0]))
    legend = ['loss']
    i = 0
    for y in lstm_net.y_list:
        plt.plot(y, '.')
        i += 1
        legend.append('y_' + str(i))
    plt.plot(loss)
    plt.legend(legend)
    plt.show()


if __name__ == "__main__":
    example_0()

