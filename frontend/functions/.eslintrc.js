module.exports = {
    env: {
        node: true,
        commonjs: true, // ✅ Add this
        es2021: true,
    },
    extends: [
        "eslint:recommended",
        "google",
    ],
    parserOptions: {
        ecmaVersion: 12,
    },
    rules: {
        // You can still customize rules here if needed
    },
};
