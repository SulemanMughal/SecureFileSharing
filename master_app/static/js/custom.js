var totalSizeLimit = 100*1024*1024;
function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'
    const k = 1000
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}
Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#my-dropzone',{
    maxFilesize: 50*1024*1024,
})
myDropzone.on('sending', function(file, xhr, formData){
    formData.append('expire', $("select#expsel").val());
    formData.append('autodestroy', $("#autodestroy").prop("checked"));
    formData.append('randomizefn', $("#randomizefn").prop("checked"));
    formData.append('shorturl', $("#shorturl").prop("checked"));
});
myDropzone.on("uploadprogress", function(file, progress, bytesSent) {
    var alreadyUploadedTotalSize = getTotalPreviousUploadedFilesSize();
    if((alreadyUploadedTotalSize + bytesSent) > totalSizeLimit){
        this.disable();
        alert("Uploading Exceeding from Limit.")
    }
});
function getTotalPreviousUploadedFilesSize(){
var totalSize = 0;
myDropzone.getFilesWithStatus(Dropzone.SUCCESS).forEach(function(file){
    totalSize = totalSize + file.size;
});
    return totalSize;
}
myDropzone.on("success", function(file, responseText) {
    $("ul#upload-filelist").prepend(
        `
        <li class="file " data-filename="${responseText['File Access URL']}">
            <span class="file-name">${file.name}</span>
            <div class="file-progress progress-outer">
                <div class="progress-inner" style="width: 100%;"></div>
            </div>

            <span class="file-url">
                <a href="${responseText['File Access URL']}" target="_BLANK">${responseText['File Access URL']}</a>
                <span>
                    <a href="/manage/${responseText["File ID"]}" target="_BLANK">manage</a>
                </span>
            </span>
        </li>
        `
    );
    $("ul#upload-filelist").removeClass("d-none")
    $("span.file-size").html(formatBytes(getTotalPreviousUploadedFilesSize()))
});