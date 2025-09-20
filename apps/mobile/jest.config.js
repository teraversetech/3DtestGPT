module.exports = {
  preset: "jest-expo",
  setupFilesAfterEnv: ["@testing-library/jest-native/extend-expect"],
  transformIgnorePatterns: [],
  transform: {
    "^.+\\.[tj]sx?$": "babel-jest"
  },
  moduleNameMapper: {
    "^@react-native-async-storage/async-storage$": "<rootDir>/__mocks__/@react-native-async-storage/async-storage.js"
  }
};
