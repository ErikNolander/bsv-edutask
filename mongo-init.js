db = db.getSiblingDB('edutask_test');

db.createCollection("test_users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["firstName", "lastName", "email"],
      additionalProperties: false,
      properties: {
        firstName: { bsonType: "string" },
        lastName: { bsonType: "string" },
        email: { bsonType: "string", pattern: "^.+@.+\\..+$" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});