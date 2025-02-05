import { StatusBar } from 'expo-status-bar';
import { Text, View } from 'react-native';
import Task from '../components/Task';
import styles from '../app/App.component.style';
import Form from '../components/Form/index';
import React, { useState } from 'react';

export default function AddPerformerScreen() {
      const [refreshTrigger, setRefreshTrigger] = useState(0);

      const handlePostSuccess = () => {
            setRefreshTrigger(prev => prev + 1);
      };

      return (
            <View style={styles.container}>

                  <Form onPostSuccess={handlePostSuccess} />

                  <StatusBar style="auto" />
            </View>
      );
}