
/**
 * Lazy function to print a message in the javascript console
 * as I kept forgetting the syntax for writeln() ...
 */
 function print(msg){
    $.writeln(msg)
}

// FROM Smart Import.jx
function testForSequence(files) {
    var searcher = new RegExp("[0-9]+");
    var movieFileSearcher = new RegExp("(mov|avi|mpg)$", "i");
    var parseResults = new Array;

    // Test that we have a sequence. Stop parsing after 10 files.
    for (x = 0;
        (x < files.length) & x < 10; x++) {
        var movieFileResult = movieFileSearcher.exec(files[x].name);
        if (!movieFileResult) {
            var currentResult = searcher.exec(files[x].name);
            // Regular expressions return null if no match was found.
            // Otherwise, they return an array with the following information:
            // array[0] = the matched string.
            // array[1..n] = the matched capturing parentheses.

            if (currentResult) { // We have a match -- the string contains numbers.
                // The match of those numbers is stored in the array[1].
                // Take that number and save it into parseResults.
                parseResults[parseResults.length] = currentResult[0];
            } else {
                parseResults[parseResults.length] = null;
            }
        } else {
            parseResults[parseResults.length] = null;
        }
    }
    // If all the files we just went through have a number in their file names,
    // assume they are part of a sequence and return the first file.

    var result = null;
    for (j = 0; j < parseResults.length; ++j) {
        if (parseResults[j]) {
            if (!result) {
                result = files[j];
            }
        } else {
            // In this case, a file name did not contain a number.
            result = null;
            break;
        }
    }

    return result;
}

function importSafeWithError(importOptions) {
    try {
        return app.project.importFile(importOptions);
    } catch (error) {
        alert(error.toString() + importOptions.file.fsName, scriptName);
    }
}

function getFolder(path, create) {
    path = path.replace(/^\/+/, "");
    path = path.replace(/\/+$/, "");
    create = (typeof create !== 'undefined') ?  create : false;

    var folderNames = path.split("/");

    if (folderNames.length == 0)
        return null;

    var folderName = folderNames[0];
    var folder = null;
    var parent = null;

    for (var i = 1;  i <= app.project.items.length; i++) {
        if (app.project.items[i].name == folderName && app.project.items[i] instanceof FolderItem) {
            parent = app.project.items[i];
            break;
        }
    }

    if (parent == null && create) {
        parent = app.project.items.addFolder(folderName);
    }

    folder = parent;

    for (var i = 1; folder !== null && i < folderNames.length; i++) {
        folder = null;

        for (var j = 1; j <= parent.numItems; j++) {
            if (parent.items[j].name == folderNames[i] && parent.items[j] instanceof FolderItem) {
                parent = parent.items[j];
                folder = parent;
                break;
            }
        }
        if (folder == null && create) {
            folder = app.project.items.addFolder(folderNames[i]);
            folder.parentFolder = parent;
            parent = folder;
        }
    }

    return folder;
}

function getMasterComp(compName) {
    comp = null;

    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.items[i].name == compName && app.project.items[i] instanceof CompItem) {
            comp = app.project.items[i];
            break;
        }
    }

    return comp;
}

function setupScene(scenePath, masterCompName, width, height, duration) {
    if (app.project != null && (app.project.file != null || app.project.dirty)) {
        var close = confirm("AfterEffects must be closed before the scene can be initialised. Save and close the current project ?");
        if (close)
            app.project.close(CloseOptions.SAVE_CHANGES);
        else
            throw new Error();
    }

    scene = File(scenePath);
    app.open(scene);

    app.project.bitsPerChannel = 16;
    app.project.workingSpace = "";
    app.project.workingGamma = "2.2";
    app.project.GpuAccelType = GpuAccelType.SOFTWARE;

    // Create master composition
    var masterComp = app.project.items.addComp(masterCompName, width, height, 1, duration/24, 24);
    masterComp.label = 9;
}

function saveScene() {
    app.project.save();
}

function importBackground(backgroundPath, width, height, duration, masterCompName) {
    // Get required folders
    var composFolder = getFolder("01 - COMPOS", true);
    var bgSourcesFolder = getFolder("02 - SOURCES/BG", true);

    // Import file
    var file = File(backgroundPath);
    var io = new ImportOptions(file);
    io.importAs = ImportAsType.COMP;
    var bgSourceComp = app.project.importFile(io);
    bgSourceComp.parentFolder = bgSourcesFolder;
    bgSourceComp.label = 9;

    // Create composition with background dimensions
    var bgComp = composFolder.items.addComp("BACKGROUND", bgSourceComp.width, bgSourceComp.height, 1, duration/24, 24);
    bgComp.label = 9;

    bgLayersFolder = getFolder(bgSourceComp.name + " Calques");

    if (bgLayersFolder !== null) {
        bgLayersFolder.parentFolder = bgSourcesFolder;
        bgLayersFolder.label = 9;
    }

    // Filter layers
    var bgGuideLayers = [];

    for (var i = bgSourceComp.numLayers; i > 0; i--) {
        var bgLayer = bgSourceComp.layers[i];

        if (bgLayer.name.match(/\s*(EXTRA.*|BG)\s*/)) {
            // Main layer
            bgLayer.label = 9;
            bgLayer.copyToComp(bgComp);
        } else {
            // Guide layer
            bgLayer.label = 0;
            bgLayer.guideLayer = true;
            bgGuideLayers.push(bgLayer);
        }
    }

    // Update master composition

    var masterComp = getMasterComp(masterCompName);

    if (masterComp !== null) {
        // Deselect existing layers
        for (var i = 1; i <= masterComp.numLayers; i++)
            masterComp.layers[i].selected = false;
        
        // Copy guide layers
        for (var i = 0; i < bgGuideLayers.length; i++) {
            bgGuideLayers[i].copyToComp(masterComp);

            bgLayerCopy = masterComp.layer(1);
            print(bgLayerCopy.name);
            bgLayerCopy.enabled = false;
            bgLayerCopy.property("position").setValue([width/2.0, height/2.0, 0.0]);
            bgLayerCopy.property("scale").setValue([71.0, 71.0, 0.0]);
        }

        // Add main layer composition
        backgroundLayer = masterComp.layers.add(bgComp);
        backgroundLayer.property("scale").setValue([71.0, 71.0, 0.0]);
        backgroundLayer.moveToEnd();
    }
}

function importAnimatic(animaticPath, masterCompName) {
    var file = File(animaticPath);
    var io = new ImportOptions(file);
    var animaticFile = app.project.importFile(io);
    animaticFile.parentFolder = getFolder("02 - SOURCES", true);

    var masterComp = getMasterComp(masterCompName);

    if (masterComp !== null) {
        antcLayer = masterComp.layers.add(animaticFile);
        antcLayer.name = "ANIMATIC";
        antcLayer.label = 0;
        antcLayer.guideLayer = true;
        antcLayer.enabled = false;
        antcLayer.property("anchorPoint").setValue([0.0, 0.0, 0.0]);
        antcLayer.property("position").setValue([0.0, 0.0, 0.0]);
        antcLayer.property("scale").setValue([71.0, 71.0, 0.0]);
        antcLayer.moveToBeginning();
    }
}

function importVideoRef(videoRefPath, masterCompName) {
    var file = File(videoRefPath);
    var io = new ImportOptions(file);
    var refFile = app.project.importFile(io);
    refFile.parentFolder = getFolder("02 - SOURCES", true);

    var masterComp = getMasterComp(masterCompName);

    if (masterComp !== null) {
        refLayer = masterComp.layers.add(refFile);
        refLayer.name = "REF";
        refLayer.label = 0;
        refLayer.guideLayer = true;
        refLayer.enabled = false;
        refLayer.property("anchorPoint").setValue([0.0, 0.0, 0.0]);
        refLayer.property("position").setValue([0.0, 0.0, 0.0]);
        refLayer.property("scale").setValue([71.0, 71.0, 0.0]);
        refLayer.moveToBeginning();
    }
}

function importAudio(audioPath, masterCompName) {
    var file = File(audioPath);
    var io = new ImportOptions(file);
    var audioFile = app.project.importFile(io);
    audioFile.parentFolder = getFolder("02 - SOURCES", true);
    audioFile.label = 12;

    var masterComp = getMasterComp(masterCompName);

    if (masterComp !== null) {
        audioLayer = masterComp.layers.add(audioFile);
        audioLayer.moveToEnd();
    }
}

function importLayers(layerLabels, layerFolders, width, height, duration, masterCompName) {
    var layersComposFolder = getFolder("01 - COMPOS/ANIM", true);
    var layersFolder = getFolder("02 - SOURCES/ANIM", true);
    var layersCompos = [];

    for (var i = 0; i < layerFolders.length; i++) {
        var sequenceFolders = layerFolders[i];
        var layersComp = layersComposFolder.items.addComp(layerLabels[i], width, height, 1, duration/24, 24);
        layersComp.label = 11;

        // Import image sequences
        for (var j = 0; j < sequenceFolders.length; j++) {
            var files = Folder(sequenceFolders[j]).getFiles();
            var sequenceStartFile = testForSequence(files);

            var io = new ImportOptions(sequenceStartFile);
            io.sequence = true;
            var importedFile = importSafeWithError(io);
            importedFile.parentFolder = layersFolder;
            importedFile.mainSource.conformFrameRate = 24;
            importedFile.label = 11;

            var animLayer = layersComp.layers.add(importedFile);
            animLayer.label = 11;
        }

        layersCompos.push(layersComp);
    }

    var masterComp = getMasterComp(masterCompName);

    if (masterComp !== null) {
        for (i = layersCompos.length - 1; i >= 0; i--) {
            masterComp.layers.add(layersCompos[i]);
        }
    }
}

// initialiseShot("TS_test", "c999", "s010", 4096, 1743, 106)