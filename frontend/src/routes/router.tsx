import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "../components/layout/AppLayout";
import { HomePage } from "../pages/HomePage";
import { CsvUploadPage } from "../pages/CsvUploadPage";
import { HealthCheckPage } from "../pages/HealthCheckPage";

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
                path: "csv-upload",
                element: <CsvUploadPage />,
            },
        ],
    },
]);