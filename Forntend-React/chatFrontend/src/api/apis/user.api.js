import { $axios } from "../axios";

export const loginUser = async (values) => {
  return await $axios.post("/login", values);
};
