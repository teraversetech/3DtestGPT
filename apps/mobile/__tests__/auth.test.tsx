import React from "react";
import { render } from "@testing-library/react-native";
import AuthScreen from "../app/index";

describe("AuthScreen", () => {
  it("renders login CTA", () => {
    const tree = render(<AuthScreen />);
    expect(tree.getByText(/Fashion3D/i)).toBeTruthy();
  });
});
