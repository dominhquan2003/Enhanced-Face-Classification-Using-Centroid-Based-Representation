import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import Task from '../components/Task';
import styles from '../app/App.component.style';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const router = useRouter();

  const handlePostSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <Task refreshTrigger={refreshTrigger} />
      </View>

      <TouchableOpacity onPress={() => router.push('/add-performer')}>
        <View style={styles.iconWrapper}>
          <Text style={styles.icon}>+</Text>
        </View>
      </TouchableOpacity>

      <StatusBar style="auto" />
    </View>
  );
}