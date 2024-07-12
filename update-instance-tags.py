import json
import jsonpath_ng as jsonpath
import logging
import colorlog
import requests as client

# Setup colored logging
log = logging.getLogger('UpdateInstanceTags')
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s: %(name)s: %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))
log.addHandler(handler)
log.setLevel(logging.DEBUG)


def update_instance_tags():
    INSTANCE_API = client.get('https://spec.wiremockapi.cloud/instance')
    CONFIG_SPEC = client.get('https://spec.wiremockapi.cloud/configspec')
    
    INSTANCE_API = INSTANCE_API.json()
    CONFIG_SPEC = CONFIG_SPEC.json()
    
    JSONPATH = jsonpath.parse('$.instance.containerDetails[0].server.sourceImage.id')
    match = JSONPATH.find(INSTANCE_API)
    if not match:
        log.error("Failed to find the sourceImage.id in the instance JSON data")
        return
    
    source_image_id = match[0].value
    log.info(f"Extracted sourceImage.id: {source_image_id}")

   # CONFIG_SPEC = json.loads(CONFIG_SPEC)
    
    # Update the metadata tag value
    for metadata in CONFIG_SPEC.get('metadata', []):
        if metadata.get('name') == 'decision':
            metadata['value'] = source_image_id
            log.info(f"Updated 'decision' tag value to: {source_image_id}")
            break

    # Convert the configspec JSON back to the original format
    UPDATED_SPEC = json.dumps(CONFIG_SPEC)
    log.info(f"Updated config spec: ${UPDATED_SPEC}")

if __name__ == "__main__":
    update_instance_tags()