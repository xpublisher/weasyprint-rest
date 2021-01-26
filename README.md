<div align="center">
	<p>
		<a href="https://github.com/xpublisher/weasyprint-rest#is=awesome">
			<img width="90%" src="https://raw.githubusercontent.com/xpublisher/weasyprint-rest/main/resources/logo_background.svg?sanitize=true"/>
		</a>
	</p>
	<p>
		<a href="https://github.com/xpublisher/weasyprint-rest/actions?query=workflow%3A%22Build%2C+Test%2C+Lint%2C+Publish%22">
			<img src="https://github.com/xpublisher/weasyprint-rest/workflows/Build,%20Test,%20Lint,%20Publish/badge.svg" alt="Build, Test, Lint, Publish"/>
		</a>
    <a href="https://codeclimate.com/github/xpublisher/weasyprint-rest/maintainability">
      <img src="https://api.codeclimate.com/v1/badges/f761c1ed2e2694f98e9c/maintainability" alt="Maintainability" />
    </a>
    <a href="https://sonarcloud.io/dashboard?id=xpublisher_weasyprint-rest">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=xpublisher_weasyprint-rest&amp;metric=alert_status" alt="Quality Gate Status">
    </a>
    <a href="https://app.dependabot.com/">
      <img src="https://img.shields.io/badge/Dependabot-active-brightgreen.svg?logo=dependabot" alt="Dependabot active">
    </a>
	</p>
	<p>
	  <a href="https://codeclimate.com/github/xpublisher/weasyprint-rest/test_coverage">
      <img src="https://api.codeclimate.com/v1/badges/f761c1ed2e2694f98e9c/test_coverage" alt="Test coverage" />
    </a>
    <a href="https://sonarcloud.io/dashboard?id=xpublisher_weasyprint-rest">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=xpublisher_weasyprint-rest&amp;metric=security_rating" alt="Security Rating">
    </a>
    <a href="https://sonarcloud.io/dashboard?id=xpublisher_weasyprint-rest">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=xpublisher_weasyprint-rest&amp;metric=reliability_rating" alt="Reliability Rating">
    </a>
    <a href="https://sonarcloud.io/dashboard?id=xpublisher_weasyprint-rest">
      <img src="https://sonarcloud.io/api/project_badges/measure?project=xpublisher_weasyprint-rest&amp;metric=vulnerabilities" alt="Vulnerabilities">
    </a>
	</p>
	<hr>
	<p>
		Service and docker image for <a href="https://weasyprint.org/">WeasyPrint - the awesome document factory</a>
	</p>
</div>

## Usage

First, you can start the container using the following command:

```bash
docker run -p 5000:5000 -d xpublisher/weasyprint-rest:latest
```

Then you can use the following command to generate the report.pdf from the official WeasyPrint sample. You can find the files in `tests/resources/report`.

```bash
curl  \
-F 'html=@report.html' \
-F 'style=@report.css' \
-F "asset[]=@FiraSans-Bold.otf" \
-F "asset[]=@FiraSans-Italic.otf" \
-F "asset[]=@FiraSans-LightItalic.otf" \
-F "asset[]=@FiraSans-Light.otf" \
-F "asset[]=@FiraSans-Regular.otf" \
-F "asset[]=@heading.svg" \
-F "asset[]=@internal-links.svg" \
-F "asset[]=@multi-columns.svg" \
-F "asset[]=@report-cover.jpg" \
-F "asset[]=@style.svg" \
-F "asset[]=@table-content.svg" \
-F "asset[]=@thumbnail.png" \
-F "mode=png" \
http://localhost:5000/api/v1.0/print --output report.png
```

## Configuration



All configurations are set via environment variables.

| Name                               | Default  | Description
|------------------------------------|----------|------------
| `API_KEY`                          | `""`     | Sets an API key that protects the `/api/v1.0/print` service from unauthorized access. The key is later compared with the header `X_API_KEY`. If no API_KEY is set, anyone can access the application.
| `BLOCKED_URL_PATTERN`              | `"^.*$"` | Pattern to block certain URLs. These URLs are later not allowed within resources of the print service. These resources will be ignored.
| `ALLOWED_URL_PATTERN`              | `"^$"`   | Pattern to allow certain URLs. These URLs are later allowed within resources of the print service.
| `MAX_UPLOAD_SIZE`                  | `16777216` | Maximum size of the upload. Default is `16MB`

## Services

### Health

Service to check if the service is still working properly.

```http
GET /api/v1.0/health
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `ping` | `string` | __Optional__. Returns the `ping` in the field `pong` |

#### Response

```javascript
{
  "status"    : "OK",
  "timestamp" : number,
  "pong"      : string?
}
```

The `status` does always contain "OK".

The `timestamp` does contain the current timestamp of the server in milliseconds.

The `pong` is optional and will only be sent if the `ping` parameter was passed. It contains the same value that `ping` had.

### Print

Service to print a pdf or png

```http
POST /api/v1.0/print
```

#### Parameters

| Parameter  | Type             |      |
|-:----------|-:----------------|-:----|
| `html`     | `file or string` | __Required__. HTML file to convert. |
| `mode`     | `"pdf" or "png"` | __Optional__. Controls whether a PDF or PNG is rendered. The default is `pdf`. |
| `template` | `string`         | __Optional__. Template name for the use of predefined templates. |
| `style`    | `file or string` | __Optional__. Style to apply to the `html`. This should only be used if the CSS is not referenced in the html. If it is included via HTML link, it should be passed as `asset`. Only either `style` or `style[]` can be used.|
| `style[]`  | `file or file[]` | __Optional__. Multiple styles to apply to the `html`. This should only be used if the CSS is not referenced in the html. If it is included via HTML link, it should be passed as `asset`. Only either `style` or `style[]` can be used.|
| `asset[]`  | `file or file[]` | __Optional__. Assets which are referenced in the html. This can be images, CSS or fonts. The name must be 1:1 the same as used in the files. |


#### Response

Raw output stream of with `Content-Type` of `application/pdf` or `image/png`. For `pdf` also the header `Content-Disposition = 'inline;filename={HTML_FILE_NAME}.pdf` will be set.
