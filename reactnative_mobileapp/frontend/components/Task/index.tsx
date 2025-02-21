import { View, Text, TouchableOpacity, FlatList, Alert } from 'react-native';
import React, { useState, useEffect } from 'react';
import styles from './task.style';
import { router } from 'expo-router';
import { useTaskContext } from '../../context/TaskContext';
import FontAwesome from '@expo/vector-icons/FontAwesome';
const Task = () => {
  const { tasks, deleteTask } = useTaskContext();

  const handleDelete = (id: number) => {
    Alert.alert(
      "Delete Task",
      "Are you sure you want to delete this task?",
      [
        { text: "Cancel", style: "cancel" },
        { text: "OK", onPress: () => deleteTask(id) }
      ]
    );
  };
  type ItemProps = {
    item: { id: number, name: string };
    index: number;
  };
  const renderItem = ({ item, index }: ItemProps) => (

    <TouchableOpacity style={styles.shadowContainer} onPress={() => router.push(`/performer/${item.id}`)}>
      <View style={styles.item}>
        <View style={styles.square}>
          <Text style={styles.number}>{index + 1}</Text>
        </View>
        <Text style={styles.content}>{item.name}</Text>
        <TouchableOpacity onPress={() => handleDelete(item.id)}>
          <FontAwesome name="trash-o" style={styles.iconTrash} />
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );
  if (tasks.length === 0) {
    return <Text>No Performers available</Text>;
  }
  return (
    <FlatList
      data={tasks}
      renderItem={renderItem}
      keyExtractor={(item, index) => index.toString()}
    />
  );
};

export default Task;
