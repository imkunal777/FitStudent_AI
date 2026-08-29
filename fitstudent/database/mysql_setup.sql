-- FitStudent AI - MySQL Database Setup Script
-- Run this script once to create the database and all tables.

CREATE DATABASE IF NOT EXISTS fitstudent_ai
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE fitstudent_ai;

-- -------------------------------------------------------
-- TABLE 1: users
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id              INT             NOT NULL AUTO_INCREMENT,
    name            VARCHAR(120)    NOT NULL,
    age             INT             NOT NULL,
    gender          VARCHAR(20)     NOT NULL,
    height          FLOAT           NOT NULL COMMENT 'Height in centimetres',
    weight          FLOAT           NOT NULL COMMENT 'Weight in kilograms',
    activity_level  VARCHAR(40)     NOT NULL,
    fitness_goal    VARCHAR(60)     NOT NULL,
    fitness_level   VARCHAR(30)     NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------
-- TABLE 2: diet_preferences
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS diet_preferences (
    id                  INT             NOT NULL AUTO_INCREMENT,
    user_id             INT             NOT NULL,
    diet_type           VARCHAR(40)     NOT NULL,
    budget              VARCHAR(30)     NOT NULL,
    preferred_foods     TEXT,
    disliked_foods      TEXT,
    cultural_preference VARCHAR(60),
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_diet_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------
-- TABLE 3: workout_preferences
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_preferences (
    id                  INT             NOT NULL AUTO_INCREMENT,
    user_id             INT             NOT NULL,
    daily_workout_time  INT             NOT NULL COMMENT 'Minutes per day',
    available_equipment VARCHAR(60)     NOT NULL,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_workout_pref_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------
-- TABLE 4: workout_plans
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_plans (
    id          INT         NOT NULL AUTO_INCREMENT,
    user_id     INT         NOT NULL,
    plan_data   LONGTEXT    NOT NULL COMMENT 'JSON-encoded weekly plan',
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_workout_plan_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------
-- TABLE 5: meal_plans
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS meal_plans (
    id          INT         NOT NULL AUTO_INCREMENT,
    user_id     INT         NOT NULL,
    plan_data   LONGTEXT    NOT NULL COMMENT 'JSON-encoded daily meal plan',
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_meal_plan_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------
-- TABLE 6: progress
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS progress (
    id                  INT             NOT NULL AUTO_INCREMENT,
    user_id             INT             NOT NULL,
    weight              FLOAT           NOT NULL,
    workout_completed   TINYINT(1)      NOT NULL DEFAULT 0,
    notes               TEXT,
    record_date         DATE            NOT NULL,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
