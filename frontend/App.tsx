import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView } from 'react-native';
import Task from './components/Task';
import styles from './App.component.style';
import Form from './components/Form/index';
export default function App() {
  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <Text style={styles.header}>List of Performers </Text>
          <Task/>   
      </View>
      <Form />

      <StatusBar style="auto" />
    </View>
  );
}

