module.exports = {
  preset: "jest-expo",
  setupFilesAfterEnv: ["@testing-library/jest-native/extend-expect"],
  transformIgnorePatterns: ["node_modules/(?!(@react-native|react-native|expo-.*|@expo|expo-three)/)"]
};
