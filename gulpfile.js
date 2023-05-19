const gulp = require("gulp");
const webpack = require("webpack-stream");
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require("autoprefixer");
const cleanCSS = require("gulp-clean-css");
const postcss = require("gulp-postcss");
const browsersync = require("browser-sync");

const dist = "./dist";
const html_templates = "./main/templates/main"
const static = "./main/static/main"


gulp.task("copy-html", () => {
    return gulp.src("./src/*.html")
                .pipe(gulp.dest(html_templates))
                .pipe(browsersync.stream());
});

gulp.task("build-js", () => {
    return gulp.src("./src/js/script.js")
                .pipe(webpack({
                    mode: 'development',
                    output: {
                        filename: 'script.js'
                    },
                    watch: false,
                    devtool: "source-map",
                    module: {
                        rules: [
                          {
                            test: /\.m?js$/,
                            exclude: /(node_modules|bower_components)/,
                            use: {
                              loader: 'babel-loader',
                              options: {
                                presets: [['@babel/preset-env', {
                                    debug: true,
                                    corejs: 3,
                                    useBuiltIns: "usage"
                                }]]
                              }
                            }
                          }
                        ]
                      }
                }))
                .pipe(gulp.dest(static + '/js'))
                .pipe(browsersync.stream());
});

gulp.task("build-sass", () => {
    return gulp.src("./src/scss/**/*.scss")
                .pipe(sass().on('error', sass.logError))
                .pipe(gulp.dest(static + '/css'))
                .pipe(browsersync.stream());
});

gulp.task("copy-assets", () => {
    gulp.src("./src/icons/**/*.*")
        .pipe(gulp.dest(static + "/icons"));

    return gulp.src("./src/img/**/*.*")
                .pipe(gulp.dest(static + "/img"))
                .pipe(browsersync.stream());
});

gulp.task("watch", () => {
    browsersync.init({
		server: "./main/staic/main/",
		port: 4000,
		notify: true
    });

    gulp.watch("./src/*.html", gulp.parallel("copy-html"));
    gulp.watch("./src/icons/**/*.*", gulp.parallel("copy-assets"));
    gulp.watch("./src/img/**/*.*", gulp.parallel("copy-assets"));
    gulp.watch("./src/scss/**/*.scss", gulp.parallel("build-sass"));
    gulp.watch("./src/js/**/*.js", gulp.parallel("build-js"));
});

gulp.task("build", gulp.parallel("copy-html", "copy-assets", "build-sass", "build-js"));

gulp.task("prod", () => {
    gulp.src("./src/*.html")
        .pipe(gulp.dest(html_templates));
    gulp.src("./src/img/**/*.*")
        .pipe(gulp.dest(static + "/img"));
    gulp.src("./src/icons/**/*.*")
        .pipe(gulp.dest(static + "/icons"));

    gulp.src("./src/js/script.js")
        .pipe(webpack({
            mode: 'production',
            output: {
                filename: 'script.js'
            },
            module: {
                rules: [
                  {
                    test: /\.m?js$/,
                    exclude: /(node_modules|bower_components)/,
                    use: {
                      loader: 'babel-loader',
                      options: {
                        presets: [['@babel/preset-env', {
                            debug: false,
                            corejs: 3,
                            useBuiltIns: "usage"
                        }]]
                      }
                    }
                  }
                ]
              }
        }))
        .pipe(gulp.dest(dist + '/js'));
    
    return gulp.src("./src/scss/style.scss")
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss([autoprefixer()]))
        .pipe(cleanCSS())
        .pipe(gulp.dest(dist + '/css'));
});

gulp.task("default", gulp.parallel("watch", "build"));