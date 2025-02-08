import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Định nghĩa kiểu cho context
interface TaskContextType {
  tasks: any[];
  addTask: (newTask: { id: number; name: string }) => void;
  fetchTasks: () => Promise<void>;
}

// Tạo Context và cung cấp giá trị mặc định
const TaskContext = createContext<TaskContextType>({
  tasks: [],
  addTask: () => {}, // Hàm giả để tránh lỗi
  fetchTasks: async () => {}, // Hàm giả để tránh lỗi
});


interface TaskProviderProps {
  children: ReactNode;
}

// Provider
export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const [tasks, setTasks] = useState<any[]>([]);


  const fetchTasks = async () => {
    try {
      const response = await fetch(process.env.EXPO_PUBLIC_API_URL);
      if (!response.ok) {
        throw new Error('Lỗi khi fetch dữ liệu');
      }
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Lỗi:', error);
    }
  };

  const addTask = (newTask: { id: number; name: string }) => {
    setTasks((prevTasks) => [...prevTasks, newTask]);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <TaskContext.Provider value={{ tasks, addTask, fetchTasks }}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTaskContext = () => {
  return useContext(TaskContext);
};