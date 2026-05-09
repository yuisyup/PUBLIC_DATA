import { Link } from "react-router-dom";

type MenuItem = {
    label: string;
    path: string;
};

type Props = {
    title: string;
    items: MenuItem[];
};

export function MenuSection({ title, items }: Props) {
    return (
        <div>
            <p className="h4 bg-secondary text-light p-2">
                {title}
            </p>

            <div className="url_area d-flex flex-column gap-2">
                {items.map((item) => (
                    <Link key={item.path} to={item.path}>
                        {item.label}
                    </Link>
                ))}
            </div>
        </div>
    );
}