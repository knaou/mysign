const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

const config = {
    entry: './src/index.js',
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: ['babel-loader','vue-loader'],
            }, {
                test: /\.js$/,
                exclude: [/node_modules/],
                use: ['babel-loader']
            }, {
                test: /\.less$/,
                use: ['style-loader','css-loader','less-loader']
            }, {
                test: /\.css$/,
                use: ['style-loader','css-loader']
            }, {
                test: /\.(png|otf|eot|svg|ttf|woff|woff2)$/,
                use: ['file-loader?name=static/[name].[ext]']
            }
            , {
                test: /\.html$/,
                use: ['file-loader?name=[name].[ext]']
            }
        ]
    },
    stats: {
        colors: true
    }
};

if (process.env.NODE_ENV === 'production') {
    config.output = {
        path: path.resolve(__dirname, '../build/'),
        filename: 'index.bundle.js'
    };
    config.resolve = {
        alias: {
            vue: 'vue/dist/vue.min.js',
            vuex: 'vuex/dist/vuex.js',
            vue_router: 'vue-router/dist/vue-router.min.js',
            vue_material: 'vue-material/dist/vue-material.js',
            axios: 'axios/dist/axios.min.js',
            vue_axios: 'vue-axios/dist/vue-axios.min.js'
        }
    };
    config.plugins = [
        new UglifyJSPlugin({
            sourceMap: false
        })
    ];
    config.devtool = false;
} else {
    config.output = {
        publicPath: '/',
        path: path.resolve(__dirname, '../build/'),
        filename: 'index.bundle.js'
    };
    config.resolve = {
        alias: {
            vue: 'vue/dist/vue.js',
            vuex: 'vuex/dist/vuex.js',
            vue_router: 'vue-router/dist/vue-router.js',
            vue_material: 'vue-material/dist/vue-material.js',
            axios: 'axios/dist/axios.js',
            vue_axios: 'vue-axios/dist/vue-axios.min.js'
        }
    };
    config.devServer = {
      host: 'localhost',
      port: 8080,
      proxy: {
        '/api': {
          target: 'http://localhost:8000'
        }
      }
    };
    config.devtool = 'inline-source-map';
}

module.exports = config;
