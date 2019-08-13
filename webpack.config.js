const path = require("path")
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const TerserJSPlugin = require('terser-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin')

module.exports = {

    context: __dirname,

    entry: {
        base: './cohort_manager/static/cohort_manager/js/base.js',
    },

    optimization: {
        minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /node_modules/,
                    chunks: "initial",
                    name: "vendor",
                    priority: 10,
                    enforce: true
                }
            }
        }
    },

    output: {
        path: path.resolve('./cohort_manager/static/cohort_manager/bundles/'),
        filename: "[name]-[hash].js",
    },

    plugins: [
        new CleanWebpackPlugin(),
        new BundleTracker({
            filename: './cohort_manager/static/webpack-stats.json'
        }),
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({
            filename: "[name]-[hash].css",
        })
    ],

    module: {
        rules: [{
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.s[ac]ss$/,
                use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader"]
            }
        ]
    },

    resolve: {
        extensions: ['.js']
    }

}
