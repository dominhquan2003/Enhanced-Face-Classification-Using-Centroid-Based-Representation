import { StyleSheet } from "react-native";
import color from "../contains/color";
const styles = StyleSheet.create({
      container: {
            flex: 1,
            backgroundColor: color.background,
            
      },
      body: {
            flex: 1,
            paddingTop: 20,
            paddingHorizontal: 20,
            
      },
      header: {
            fontSize: 24,
            fontWeight: 'bold',
            color: color.primary,
      },
      items: {
            marginTop: 25,
      },
      iconWrapper: {
            position: 'absolute', // Đặt position là absolute để icon nổi lên
            bottom: 20, // Khoảng cách từ đáy màn hình
            right: 20, // Khoảng cách từ bên phải
            height: 44,
            width: 44,
            backgroundColor: color.primary,
            borderRadius: 22,
            justifyContent: "center",
            alignItems: "center",
            borderWidth: 2,
            borderColor: color.primary,
            elevation: 5, // Thêm bóng đổ cho icon (Android)
            shadowColor: '#000', // Thêm bóng đổ cho icon (iOS)
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.3,
            shadowRadius: 4,
          },
          icon: {
            color: color.white,
            fontSize: 24,
            zIndex: 1, // Đảm bảo icon nằm trên cùng
          },

});
export default styles;