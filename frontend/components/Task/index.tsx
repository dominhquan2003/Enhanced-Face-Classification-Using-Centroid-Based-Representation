import { View, Text, TouchableOpacity, FlatList } from 'react-native';
import React, { useState, useEffect } from 'react';
import styles from './task.style';
import { useRouter } from 'expo-router';
// Khai báo kiểu cho props
interface TaskProps {
  refreshTrigger: number;
}

const Task = ({ refreshTrigger }: TaskProps) => {
  const router = useRouter();
  const [tasks, setTasks] = useState<any[]>([]);
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const fetchTasks = () => {
    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
        setTasks(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  useEffect(() => {
    fetchTasks();
  }, [refreshTrigger]); 

  type ItemProps = {
    item: { id: number, name: string };
    index: number;
  };

  // const getSquareStyle = (index : any) => (index + 1) % 2 === 0 ? styles.squareEven : styles.squareOdd;
  
  const renderItem = ({ item, index }: ItemProps) => (
    
    <TouchableOpacity style={styles.shadowContainer} onPress={() => router.push(`/performer/${item.id}`)}>
      <View style={styles.item}>
        {/* <View style={[styles.square, getSquareStyle(index)]}> */}
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
