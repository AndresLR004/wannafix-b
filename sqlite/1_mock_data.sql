-- Para la tabla users
INSERT INTO users (name, email, role, verified, password) VALUES
('Joan Pérez', 'joan@example.com', 'admin', 1, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
('Anna García', 'anna@example.com', 'moderator', 1, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
('Elia Rodríguez', 'elia@example.com', 'wanner', 1, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
('Kevin Salardú', 'kevin@example.com', 'wanner', 1, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4');

-- Para la tabla services
INSERT INTO services (title, description, photo, price, duration_hours, duration_days, category_id, status_id) VALUES
('Reparación de fontanería', 'Reparación de grifos y cañerías', 'fontaneria.jpg', 50.00, 2, 0, 1, 1),
('Instalación eléctrica', 'Instalación y reparación de circuitos eléctricos', 'electricidad.jpg', 80.00, 0, 1, 2, 1),
('Pintura de interiores', 'Pintura de paredes y techos', 'pintura.jpg', 120.00, 0, 3, 3, 1),
('Limpieza de hogar', 'Limpieza profunda de toda la casa', 'limpieza.jpg', 60.00, 4, 0, 4, 1),
('Reparación de electrodomésticos', 'Reparación de lavadoras, neveras, etc.', 'electrodomesticos.jpg', 70.00, 0, 2, 1, 1);

-- Para la tabla categories
INSERT INTO categories (name, slug) VALUES
('Fontanería', 'fontaneria'),
('Electricidad', 'electricidad'),
('Pintura', 'pintura'),
('Limpieza', 'limpieza'),
('Mecánica', 'mecanica'),
('Otro', 'otro');

-- Para la tabla statuses
INSERT INTO statuses (name, slug) VALUES
('Activo', 'activo'),
('Inactivo', 'inactivo');