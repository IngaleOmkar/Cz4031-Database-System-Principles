#ifndef B_PLUS_TREE_H
#define B_PLUS_TREE_H

#include "memory-pool.h"
#include <climits>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>

using namespace std;

struct keys_struct
{
  float key_value;         // Key value.
  vector<void *> add_vect; // List of records with same key.
};

class BPTree;

class Node
{
  bool isLeaf;       // Whether node is a leaf node.
  keys_struct *keys; // Pointer to array of keys in node.
  int size;          // Number of keys in node.
  Node **pointers;   // Pointer to array of pointers in node.
  friend class BPTree;

public:
  Node();
};

class BPTree
{
  Node *root;
  /**
   * @brief
   * Insert internal node.
   * @param x Key to be added to the parent node.
   * @param cursor Parent node.
   * @param child Child node.
   */
  void insertInternal(keys_struct x, Node *cursor, Node *child);

  /**
   * @brief
   * Remove internal node.
   * @param x Key of node to be removed.
   * @param cursor Parent.
   * @param child The removed node.
   * @return int Number of nodes deleted.
   */
  int removeInternal(keys_struct x, Node *cursor, Node *child);

  /**
   * @brief
   * Find parent of child.
   * @param cursor
   * @param child
   * @return Node*
   */
  Node *findParent(Node *cursor, Node *child);

  /**
   * @brief
   * Update correct parent when key is being deleted from leaf node.
   * @param child
   * @param key The new key.
   */
  void updateParent(Node *child, keys_struct key);

  /**
   * @brief
   * Get new key to be added to parent node.
   * @param cursor
   * @return keys_struct
   */
  keys_struct getNewKey(Node *cursor);
  int numNode = 0;

public:
  BPTree();
  /**
   * @brief
   * Search for the leaf node with key.
   * @param key Key value to search for.
   */
  void searchSingle(float key);

  /**
   * @brief
   * Search for leaf nodes within the key boundaries.
   * @param lowerKeyBound lower boundary of key.
   * @param upperKeyBound upper boundary of key.
   */
  void searchRange(float lowerKeyBound, float upperKeyBound);

  /**
   * @brief
   * Get height of tree.
   * @param cursor Root node
   * @return int Height of tree.
   */
  int getHeight(Node *cursor);

  /**
   * @brief
   * Inserts key into tree.
   * @param x Key to be inserted.
   */
  void insert(keys_struct x);

  /**
   * @brief
   * Removes key from tree.
   * @param x
   * @return int Number of nodes deleted.
   */
  int remove(keys_struct x);

  /**
   * @brief Get the Root object
   * Get root of tree.
   * @return Node* root.
   */
  Node *getRoot();

  int getMax();

  /**
   * @brief Get the number of nodes.
   *
   * @return int number of nodes in tree.
   */
  int getNodeNum() { return numNode; }

  /**
   * @brief
   * Use breadth first search to calculate the number of nodes in tree.
   * @param cursor
   * @return int number of nodes in tree.
   */
  int calculateNodeNum(Node *cursor);

  /**
   * @brief
   * Prints entire tree.
   * @param cursor Root node.
   */
  void printTree(Node *cursor);

  /**
   * @brief
   * Prints only root node and 1st child node.
   * @param cursor Root node.
   */
  void show(Node *cursor);
};

#endif
