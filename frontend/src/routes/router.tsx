import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "../components/layout/AppLayout";
import { HomePage } from "../pages/HomePage";
import { BulkRegisterPage } from "../pages/BulkRegisterPage";
import { HealthCheckPage } from "../pages/HealthCheckPage";
import { RunResultReferencePage } from "../pages/RunResultReferencePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "health",
        element: <HealthCheckPage />,
      },
      {
        path: "bulk-register",
        element: <BulkRegisterPage />,
      },
      {
        path: "run-result-reference",
        element: <RunResultReferencePage />,
      },
    ],
  },
]);
