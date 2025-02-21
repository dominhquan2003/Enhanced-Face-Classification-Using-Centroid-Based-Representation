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
            paddingHorizontal: 16,

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
            position: 'absolute',
            bottom: 24,
            right: 24,
            height: 50,
            width: 50,
            backgroundColor: color.primary,
            borderRadius: 22,
            justifyContent: "center",
            alignItems: "center",
            borderWidth: 2,
            borderColor: color.primary,

      },
      icon: {
            color: color.primary,
            fontSize: 30,

      },

});
export default styles;