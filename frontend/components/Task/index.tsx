import { View, Text, TouchableOpacity, FlatList } from 'react-native';
import React, { useState, useEffect } from 'react';
import styles from './style';

// Khai báo kiểu cho props
interface TaskProps {
  refreshTrigger: number;
}

const Task = ({ refreshTrigger }: TaskProps) => {
  const [tasks, setTasks] = useState<any[]>([]);

  const fetchTasks = () => {
    fetch('http://10.66.2.113:8000/facedetect/api/v1/', {
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
  }, [refreshTrigger]); // fetch lại mỗi khi refreshTrigger thay đổi

  type ItemProps = {
    item: { id: number, name: string };
    index: number;
  };

  const renderItem = ({ item, index }: ItemProps) => (
    <TouchableOpacity>
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
