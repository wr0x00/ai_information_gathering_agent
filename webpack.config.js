const path = require('path');

module.exports = {
    entry: './django_ai_agent/frontend_app/static/frontend/js/components/App.js',
    output: {
        path: path.resolve(__dirname, 'django_ai_agent/frontend_app/static/frontend/js'),
        filename: 'bundle.js',
    },
    module: {
        rules: [{
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    mode: 'development',
};