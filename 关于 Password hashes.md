# 密码散列值（ Password hashes ）
1. 问题：若要保证数据库中用户密码的安全，关键在于不能存储密码本身，而要存储密码的散列值

- 计算密码散列值的函数接收密码作为输入，使用一种或多种加密算法转换密码，最终得到一个和原始密码没有关系的字符序列。
- 核对密码时密码散列值可代替原始密码，因为计算散列值的函数是可复现的：只要输入一样，结果就一样。

---

 2.问题：计算密码散列值的函数（hash function)的原理

2.1 问题：什么是散列值函数（hash function）？Key derivation functions （KDFs）
   
- 一种从任何一种数据中创建小的数字“指纹”的方法。
- 将任意长度的数据映射到有限长度域上，对一串数据m进行杂糅，输出另一段固定长度的数据h，作为数据串m的指纹（特征）
- 从理论上说，设计良好的hash函数，对于任何不同的输入数据，都应该以极高的概率生成不同的输出数据。因此可以作为指纹使用，来判断两组数据是否相同。
- 数据 --> 输入哈函数 --> 输出指纹数据

2.2 问题：散列值函数原理
- 将数据块m分成固定长度（如128位），依次进行hash运算，然后不同的方法迭代（如前一块的hash值与后一块的hash值进行异或）
- 如果不够128位，用0或1补全（算法中约定）
-  The non-secret parameters are called "salt" in this context.


2.3 问题：hash在数据结构中的含义和密码学中的含义不同，在不同的领域，算法的侧重点不同

- __抗碰撞能力__
- __抗篡改能力__

2.3.1 问题： 数据结构中的hash

在用到hash进行管理的数据结构中（hashmap，hash值（key）），存在的目的是加速键值对的查找，hash出来的key只要保证value大致均匀的放在不同的桶里，而对于抗碰撞的要求没那么高。


此时的hash就是找到一种数据内容和数据存放地址之间的映射关系，整个算法的性能与hash值产生的速度有关。

数组的特点：寻址容易，插入和删除困难（O(n); 链表的特点：寻址困难，插入和删除容易。哈希表综合二者的特性，是一种寻址容易，插入删除也容易的数据结构。

- hash表的适用场景：

快速查找，删除的基本数据结构，通常需要总数据量可以放入内存中。hash表是一种查找效率极高的数据结构

-hash表要点：

hash函数选择，针对字符串，整数，排列具体相应的hash方法; 碰撞处理，拉链法（open hashing），开地址法（closed hashing），opened addressing。d-left hashing




2.3.2 问题：密码学中的hash

用于消息摘要和签名，对整个消息的完整性进行校验。对于抗碰撞和抗篡改能力要求极高。

-  Dk = KDF(Key, Salt, Iterations), DK is the derived key, key is the original key or password, Salt is a random number which acts as cryptographic salt, and Iterations refers to the number of iterations of a sub-function.

---
