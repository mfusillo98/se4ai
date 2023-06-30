CREATE
DATABASE software_engineering;

USE
software_engineering;

CREATE TABLE projects
(
    project_id                INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name                      VARCHAR(255) NOT NULL,
    api_key                   VARCHAR(255),
    selected_features_indexes TEXT,
    created_at                timestamp default current_timestamp,
    updated_at                timestamp default current_timestamp on update current_timestamp
);

ALTER TABLE projects CONVERT TO CHARACTER SET utf8;

CREATE TABLE project_resources
(
    resource_id          INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    project_id           INT(11) NOT NULL,
    external_resource_id TEXT,
    name                 VARCHAR(255),
    created_at           timestamp default current_timestamp,
    updated_at           timestamp default current_timestamp on update current_timestamp,
    FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE project_resources CONVERT TO CHARACTER SET utf8;

CREATE TABLE project_resource_images
(
    image_id    INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    resource_id INT(11) NOT NULL,
    url         TEXT,
    created_at  timestamp default current_timestamp,
    updated_at  timestamp default current_timestamp on update current_timestamp,
    FOREIGN KEY (resource_id) REFERENCES project_resources (resource_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE project_resource_images_raw_features
(
    image_id INT(11) NOT NULL,
    features TEXT,
    FOREIGN KEY (image_id) REFERENCES project_resource_images (image_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE project_resource_images_selected_features
(
    image_id INT(11) NOT NULL,
    features TEXT,
    FOREIGN KEY (image_id) REFERENCES project_resource_images (image_id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE projects
    ADD trained int(1) default 0;

CREATE TABLE project_train_history
(
    history_id                INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    project_id                INT(11) NOT NULL,
    selected_features_indexes TEXT,
    created_at                timestamp default current_timestamp,
    FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE project_search_performance
(
    search_id                         INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    project_id                        INT(11) NOT NULL,
    selected_features_indexes         TEXT,
    image_url                         TEXT,
    results_with_feature_selection    TEXT,
    results_without_feature_selection TEXT,
    error                             FLOAT,
    created_at                        timestamp default current_timestamp,
    FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE ON UPDATE CASCADE
);