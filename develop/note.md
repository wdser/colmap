
COLMAP_VERSION = "3.11.0.dev0"


# incremental_mapper
```c++
// IncrementalPipeline src/colmap/sfm/incremental_mapper.h
IncrementalPipeline::Reconstruct() 
    -> IncrementalPipeline::ReconstructSubModel() 
        -> IncrementalMapper::BeginReconstruction()
        -> IncrementalPipeline::InitializeReconstruction()
            ->IncrementalMapper::FindInitialImagePair()
            ->IncrementalMapper::EstimateInitialTwoViewGeometry()
            ->IncrementalMapper::RegisterInitialImagePair()
            ->IncrementalMapper::AdjustGlobalBundle()
            ->IncrementalMapper::FilterPoints()
            ->IncrementalMapper::FilterImages()
        -> IncrementalMapper::FindNextImages()
        -> IncrementalMapper::RegisterNextImage()
        -> IncrementalMapper::TriangulateImage()
            ->IncrementalTriangulator::TriangulateImage()
        -> IncrementalMapper::IterativeLocalRefinement()
        -> IncrementalPipeline::CheckRunGlobalRefinement()
        -> IncrementalPipeline::IterativeGlobalRefinement()
```

# matcher
```c++
// src/colmap/exe/feature.cc
|-> RunFeatureExtractor() 
|-> RunFeatureImporter() 
|-> RunExhaustiveMatcher() 
|-> RunMatchesImporter() 
|-> RunSequentialMatcher() 
|-> RunSpatialMatcher() 
|-> RunTransitiveMatcher() 
|-> RunVocabTreeMatcher() 
    -> Create matcher
        // src/colmap/controllers/feature_matching.cc
        |-> CreateExhaustiveFeatureMatcher()   -- ExhaustivePairGenerator::
        |-> CreateSpatialFeatureMatcher()      -- SpatialPairGenerator::
        |-> CreateSequentialFeatureMatcher()   -- SequentialPairGenerator::
        |-> CreateTransitiveFeatureMatcher()   -- TransitivePairGenerator::
        |-> CreateImagePairsFeatureMatcher()   -- ImportedPairGenerator::
        |-> CreateVocabTreeFeatureMatcher()    -- VocabTreePairGenerator::
        |-> CreateFeaturePairsFeatureMatcher() -- FeaturePairsFeatureMatcher::
    // GenericFeatureMatcher public Thread
    -> matcher->Start()
        // src/colmap/controllers/feature_matching.cc
        -> GenericFeatureMatcher::Run() // call DerivedPairGenerator 
            // src/colmap/controllers/feature_matching_utils.cc
            -> FeatureMatcherController::Setup()
            // src/colmap/feature/matcher.h
            -> FeatureMatcherCache::Setup()
                // src/colmap/controllers/feature_matching_utils.cc
                -> FeatureMatcherWorker::Run() 
                    // src/colmap/feature/matcher.h
                    // src/colmap/feature/sift.cc
                    // FeatureMatcher, SiftGPUFeatureMatcher, SiftCPUFeatureMatcher
                    |-> FeatureMatcher::Match() // verifier_queue_
                        -> ComputeSiftDistanceMatrix() 
                        -> FindBestMatchesBruteForce()
                        -> FindBestMatchesIndex()
                    |-> FeatureMatcher::MatchGuided() // output_queue_
                        -> ComputeSiftDistanceMatrix() 
                        -> FindBestMatchesIndex()

            // src/colmap/feature/pairing.cc
            -> DerivedPairGenerator::Next()
            -> FeatureMatcherController::Match() // move matcher_queue_, verifier_queue_ and save output_queue_

    -> matcher->Wait()
```

# FeatureMatcherController
```c++
// control differnet job
// src/colmap/controllers/feature_matching_utils.cc
* FeatureMatcherController::FeatureMatcherController()
    // init verifiers_, guided_matchers_, matchers_ with matcher_queue_, verifier_queue_, output_queue_, guided_matcher_queue_
    JobQueue:: matcher_queue_, verifier_queue_, output_queue_, guided_matcher_queue_
    Thread:: verifiers_
    FeatureMatcherWorker:: matchers_, guided_matchers_ 
* FeatureMatcherController::Setup()
    // start matchers_, verifiers_, guided_matchers_

* FeatureMatcherController::Match() 
    // match image_pairs:
        // 1.exists_matches: verifier
        // 2.matcher
    // check size of matches and inlier_matches, save output
```

# Thread
```c++
Thread:: // src/colmap/util/threading.cc
* Thread::Start()
    -> Thread::Wait()
    -> Thread::RunFunc // std::thread
        -> Thread::Run() // pure virtual function
* Thread::Stop()
```

# JobQueue<T>
```c++
queue<T>:: jobs_
condition_variable:: push_condition_, pop_condition_, empty_condition_
```