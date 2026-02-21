authors_spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Authors API",
        "version": "1.0.0",
        "description": "REST API для работы с авторами и их книгами."
    },
    "servers": [
        {"url": "http://127.0.0.1:5000"}
    ],
    "paths": {
        "/api/authors": {
            "get": {
                "summary": "Получить список всех авторов",
                "description": "Возвращает список всех авторов.",
                "responses": {
                    "200": {
                        "description": "Список авторов",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Author"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Создать нового автора",
                "description": "Создаёт нового автора по переданным полям.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AuthorInput"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Автор успешно создан",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Author"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Ошибка валидации данных автора"
                    }
                }
            }
        },
        "/api/authors/{id}": {
            "get": {
                "summary": "Получить книги автора",
                "description": "Возвращает все книги указанного автора.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Список книг автора",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Book"
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Автор не найден"
                    }
                }
            },
            "delete": {
                "summary": "Удалить автора и все его книги",
                "description": "Удаляет автора и все его книги (каскадно).",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Автор и книги удалены",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "Author and all books deleted"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Автор не найден"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Author": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "middle_name": {"type": "string", "nullable": True}
                }
            },
            "AuthorInput": {
                "type": "object",
                "required": ["first_name", "last_name"],
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "middle_name": {"type": "string", "nullable": True}
                }
            },
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "author_id": {"type": "integer"}
                }
            }
        }
    }
}
