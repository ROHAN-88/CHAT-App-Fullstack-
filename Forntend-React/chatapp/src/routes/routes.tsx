import {
  createRootRoute,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import Login from "../components/Login";

const rootRoute = createRootRoute();
// Define routes
const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/login",
  component: Login,
});

// Create the router
const router = createRouter({
  routeTree: rootRoute.addChildren([homeRoute]),
});

export default router;
