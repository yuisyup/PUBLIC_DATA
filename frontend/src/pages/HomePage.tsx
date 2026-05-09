import { Col, Row } from "react-bootstrap";
import { MenuSection } from "../components/menu/MenuSection";

export function HomePage() {
    return (
        <Row className="border m-3 p-3">
            <Col>
                <MenuSection
                    title="データ登録"
                    items={[
                        {
                            label: "CSV読み込み",
                            path: "/csv-upload",
                        },
                    ]}
                />
            </Col>

            <Col>
                <MenuSection
                    title="照会/分析"
                    items={[]}
                />
            </Col>
        </Row>
    );
}