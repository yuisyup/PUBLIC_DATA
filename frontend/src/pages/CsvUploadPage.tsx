import { CsvUploadForm } from "../components/form/CsvUploadForm";

export function CsvUploadPage() {
    return (
        <div>
            <div className="bg-primary text-white p-3 mb-4">
                <h1 className="mb-0">CSV読み込み</h1>
            </div>

            <CsvUploadForm />
        </div>
    );
}