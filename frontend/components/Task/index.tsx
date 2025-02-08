import { View, Text, TouchableOpacity, FlatList } from 'react-native';
import React, { useState, useEffect } from 'react';
import styles from './task.style';
import { router } from 'expo-router';
import { useTaskContext } from '../../context/TaskContext';

const Task = () => {
  const { tasks } = useTaskContext();
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
