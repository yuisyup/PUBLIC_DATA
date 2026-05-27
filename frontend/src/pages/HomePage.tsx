import { Col, Row } from "react-bootstrap";
import { MenuSection } from "../components/menu/MenuSection";

/**
 * ホームページ（メニュー）
 * @returns
 */
export function HomePage() {
  return (
    <Row className="border m-3 p-3">
      <Col>
        <MenuSection
          title="データ登録"
          items={[
            {
              label: "ファイル一括登録",
              path: "/bulk-register",
            },
          ]}
        />
      </Col>

      <Col>
        <MenuSection title="照会/分析" items={[]} />
      </Col>
      <Col>
        <MenuSection title="管理" items={[]} />
      </Col>
    </Row>
  );
}
