# 🤖 Telegram Bot on Aiogram 3.14
 
## 📋 About the Project   

Welcome to a comprehensive Telegram bot project built with **Aiogram 3.14**! This is an **open-source** solution that combines all the necessary functionality to create a full-featured Telegram bot.

> **License:** MIT License. See LICENSE file for details.

## ✨ Project Features

- 🔧 **Complete configuration setup**
- 🗄️ **Database integration**
- 🎯 **Comprehensive handler system**
- ⌨️ **Various keyboard types**
- 💰 **Payment integration preparation**
- 🔗 **Referral system**
- 📊 **External API integration examples**

## 📁 Project Structure 
![изображение](https://github.com/user-attachments/assets/7c0f717e-2064-421a-9566-25dabe59092a)

### 📂 `/config` - Configuration Files
Contains all necessary configuration files:

- **`config.py`** - main configuration with environment variable loading
- **`texts_config.py`** - all bot text messages
- **`.env`** - environment variables (*created manually*)

#### `.env` File Structure:
```env
MAIN_BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id
ADMIN_USERNAME=your_admin_username
BOT_USERNAME=your_bot_username
```

### 📂 `/scripts` - Helper Scripts
Additional scripts for extended functionality. Includes **Bitcoin price fetching example**.

### 📂 `/src` - Main Project Code

#### 📊 `database/`
**Simple and clear database system** with detailed comments.

#### 🎯 `handlers/`
**Complete set of handlers** with examples of all possible Telegram bot usage scenarios.

#### ⌨️ `keyboards/`
**Two types of keyboards:**
- **Inline keyboards** - attached to messages
- **Reply keyboards** - displayed at the bottom of the bot interface

#### 💳 `payments/`
**Payment system template.** Detailed implementation instructions are in this folder's README.

#### 🖼️ `pictures/`
**Organized image storage:**
- `main_pictures/` - main images
- `products_pictures/` - product images

#### 🛍️ `products/`
**Product management system** with simple and complex product classes.

#### 🔗 `referral_system/`
**Referral system** (main logic integrated into `db.py`).

## 🚀 Running the Project

To start the bot, run the **`main_bot.py`** file - it's implemented following all **best practices**.

## 📈 Development History

The project was developed over a **week** with detailed change logging in the Telegram channel **[@programming300days](https://t.me/programming300days)**.

# 🤖 Telegram Bot на Aiogram 3.14

## 📋 О проекте

Добро пожаловать в комплексный проект Telegram бота, построенного на **Aiogram 3.14**! Это **open-source** решение, которое объединяет в себе всю необходимую функциональность для создания полнофункционального Telegram бота.

> **Лицензия:** MIT License. Подробности в файле LICENSE.

## ✨ Особенности проекта

- 🔧 **Полная настройка конфигурации**
- 🗄️ **Интеграция с базой данных**  
- 🎯 **Комплексная система обработчиков** (handlers)
- ⌨️ **Различные типы клавиатур**
- 💰 **Подготовка к интеграции платежей**
- 🔗 **Реферальная система**
- 📊 **Примеры интеграции с внешними API**

## 📁 Структура проекта
![изображение](https://github.com/user-attachments/assets/0d0f82ca-c1b8-4e2c-9295-e30a4a01f8a1)

### 📂 `/config` - Конфигурационные файлы
Содержит все необходимые файлы конфигурации:

- **`config.py`** - основная конфигурация с загрузкой переменных окружения
- **`texts_config.py`** - все текстовые сообщения бота  
- **`.env`** - переменные окружения (*создается вручную*)

#### Структура `.env` файла:
```env
MAIN_BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id
ADMIN_USERNAME=your_admin_username
BOT_USERNAME=your_bot_username
```

### 📂 `/scripts` - Вспомогательные скрипты
Дополнительные скрипты для расширенного функционала. Включает **пример получения курса Bitcoin**.

### 📂 `/src` - Основной код проекта

#### 📊 `database/`
**Простая и понятная система работы с базой данных** с подробными комментариями.

#### 🎯 `handlers/`
**Полный набор обработчиков** с примерами всех возможных сценариев использования в Telegram ботах.

#### ⌨️ `keyboards/`
**Два типа клавиатур:**
- **Inline клавиатуры** - прикрепляются к сообщениям
- **Reply клавиатуры** - отображаются внизу интерфейса бота

#### 💳 `payments/`
**Заготовка для платежной системы.** Подробные инструкции по реализации находятся в README этой папки.

#### 🖼️ `pictures/`
**Организованное хранение изображений:**
- `main_pictures/` - основные изображения
- `products_pictures/` - изображения товаров

#### 🛍️ `products/`
**Система управления товарами** с простыми и сложными классами продуктов.

#### 🔗 `referral_system/`
**Реферальная система** (основная логика интегрирована в `db.py`).

## 🚀 Запуск проекта

Для запуска бота выполните файл **`main_bot.py`** - он реализован с учетом всех **best practices**.

## 📈 История разработки

Проект разрабатывался в течение **недели** с ведением подробного лога изменений в Telegram канале **[@programming300days](https://t.me/programming300days)**.

---
